import os
import zipfile
import shutil
import pandas as pd

class extracaoCSV():

    def extracao_csv(self):
        lista_municipios = ['AM', 'AP', 'AC', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']

        zip_folder = '../../data/brutos/clima/'
        extract_folder_base = '../../data/extracao/temporario/'
        output_folder = '../../data/extracao/anual/'
        os.makedirs(output_folder, exist_ok=True)

        for ano in range(2000, 2024):
            zip_name = f"{ano}.zip"
            zip_path = os.path.join(zip_folder, zip_name)

            if not os.path.exists(zip_path):
                print(f"Arquivo {zip_name} não encontrado.")
                continue

            print(f"\nProcessando {zip_name}...")

            extract_path = os.path.join(extract_folder_base, str(ano))

            # Remove a pasta antiga (se existir) e recria
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)
            os.makedirs(extract_path, exist_ok=True)

            # Extrai os arquivos
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            dataframes = []

            for root, _, files in os.walk(extract_path):
                for nome_arquivo in files:
                    if nome_arquivo.endswith('.CSV'):
                        caminho_arquivo = os.path.join(root, nome_arquivo)

                        try:
                            with open(caminho_arquivo, 'r', encoding='latin1') as f:
                                linhas = f.readlines()

                            uf = None
                            for linha in linhas:
                                if linha.startswith('UF:;'):
                                    uf = linha.split(';')[1].strip()
                                    break

                            if uf not in lista_municipios:
                                continue

                            partes = nome_arquivo.split('_')
                            municipio = partes[4] if len(partes) >= 5 else 'desconhecido'
                            municipio = municipio.capitalize()

                            df = pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', skiprows=8, engine='python')
                            df['municipio'] = municipio
                            df['estado'] = uf
                            dataframes.append(df)

                        except Exception as e:
                            print(f"Erro ao processar {nome_arquivo}: {e}")

            if dataframes:
                df_concatenado = pd.concat(dataframes, ignore_index=True)
                output_path = os.path.join(output_folder, f'dados-clima-{ano}.csv')
                df_concatenado.to_csv(output_path, index=False, sep=';')
            else:
                print(f"Nenhum dado válido encontrado para {ano}.")

    def extracao_final(self):
        dataframes = []
        pasta_csv = '../../data/extracao/anual/'

        for arquivo in os.listdir(pasta_csv):
            if arquivo.endswith('.csv'):
                caminho_completo = os.path.join(pasta_csv, arquivo)
                try:
                    df = pd.read_csv(caminho_completo, encoding='latin1', sep=';')
                    dataframes.append(df)
                    print(f"Lido: {arquivo}")
                except Exception as e:
                    print(f"Erro ao ler {arquivo}: {e}")

        if dataframes:
            df_final = pd.concat(dataframes, ignore_index=True)
            output_path_final = '../../data/extracao/dados-clima-final.csv'
            df_final.to_csv(output_path_final, index=False, sep=';')
            print(f"Arquivo final gerado com sucesso: {output_path_final}")
        else:
            print("Nenhum CSV foi lido para gerar o arquivo final.")
