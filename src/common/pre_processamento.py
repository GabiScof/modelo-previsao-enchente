import pandas as pd

from src.helpers.formata_csv import formataCSV
from src.helpers.formata_csv_clima import formataCSVClima

if __name__ == "__main__":
    classe = formataCSV()

    # Leitura dos dataframe de pluviometria, municipio e desmatamento
    df_ap = pd.read_csv('../../data/brutos/dados-pluviometricos-AP.csv')
    df_ac = pd.read_csv('../../data/brutos/dados-pluviometricos-AC.csv')
    df_municipios = pd.read_csv('../../data/brutos/estacao-pluviometrica-municipio.csv')
    df_desmatamento= pd.read_csv('../../data/brutos/desmatamento_por_municipio.csv')
    df_clima = pd.read_csv('../../data/extracao/dados-clima-final.csv', encoding='latin1', sep=';', engine='python')

    # Criação do dataframe de pluviometria com todos os estados
    df_pluviometria = classe.concatena_df(df_ap=df_ap, df_ac=df_ac)

    # Pré-processamento de colunas
    df_pluviometria = classe.separa_coluna_data(df=df_pluviometria)
    df_pluviometria = classe.agrupa_por_mes(df=df_pluviometria)

    # Agrupamento dos dataframes de código de município e nome de município
    df_pluviometria = classe.merge_codigo_municipio(df_codigos=df_pluviometria, df_municipios=df_municipios)

    # Pré-processamento de strings
    df_pluviometria['municipio'] = df_pluviometria['municipio'].apply(classe.formata_string)
    df_desmatamento['municipality'] = df_desmatamento['municipality'].apply(classe.formata_string)

    # Seleção das colunas do df de desmatamento
    df_desmatamento = df_desmatamento[['year', 'areakm', 'municipality']]

    # Renomeação das colunas do df de desmatamento
    df_desmatamento.rename(columns={'year': 'ano', 'municipality': 'municipio'}, inplace=True)

    # Agrupamento dos dataframes de pluviometria e desmatamento
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df_pluviometria, df_desmatamento=df_desmatamento, condicoes=['ano', 'municipio'])

    # Inclusão de dados de clima
    df_clima['municipio'] = df_clima['municipio'].apply(classe.formata_string)

    # Renomeação das colunas
    df_clima.columns = [classe.limpar_nome_coluna(c) for c in df_clima.columns]
    df_clima.rename(columns={
        "PRECIPITAAAAAO TOTAL, HORAARIO (mm)": "precipitacao_total_mm",
        "PRESSAAO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)": "pressao_max_ant_mb",
        "PRESSAAO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)": "pressao_min_ant_mb",
        "RADIACAO GLOBAL (KJ/mAA2)": "radiacao_global_kj_m2",
        "TEMPERATURA DO AR - BULBO SECO, HORARIA (AAC)": "temperatura_bulbo_seco_c",
        "TEMPERATURA DO PONTO DE ORVALHO (AAC)": "temperatura_orvalho_c",
        "TEMPERATURA MAAXIMA NA HORA ANT. (AUT) (AAC)": "temperatura_max_ant_c",
        "TEMPERATURA MAANIMA NA HORA ANT. (AUT) (AAC)": "temperatura_min_ant_c",
        "TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (AAC)": "orvalho_max_ant_c",
        "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (AAC)": "orvalho_min_ant_c",
        "umidade_max_ant_pct": "umidade_max_ant_pct",
        "umidade_min_ant_pct": "umidade_min_ant_pct",
        "umidade_ar_pct": "umidade_ar_pct",
        "VENTO, DIREAAAAO HORARIA (gr) (AA (gr))": "vento_direcao_graus",
        "vento_rajada_max_ms": "vento_rajada_max_ms",
        "vento_velocidade_ms": "vento_velocidade_ms",
        "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)": "pressao_nivel_estacao_mb",
        "UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)": "umidade_max_ant_pct",
        "UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)": "umidade_min_ant_pct",
        "UMIDADE RELATIVA DO AR, HORARIA (%)": "umidade_ar_pct",
        "VENTO, RAJADA MAXIMA (m/s)": "vento_rajada_max_ms",
        "VENTO, VELOCIDADE HORARIA (m/s)": "vento_velocidade_ms",
    }, inplace=True)

    # Remover coluna desnecessária
    df_clima = df_clima.drop(columns = ['Unnamed: 19'])

    # Agrupamento dos dataframes de pluviometria-desmatamento e clima
    df_desma_pluvio_clima = classe.agrupa_csv(df_pluviometria=df_desma_pluvio, df_desmatamento=df_clima, condicoes=['ano', 'mes', 'municipio'])

    # Exportação dos csv de pluviometria e desmatamento
    df_pluviometria.to_csv('../../data/formatados/dados-pluviometricos.csv', index=False)
    df_desma_pluvio.to_csv('../../data/formatados/dados-pluviometricos-desmatamento.csv', index=False)
    df_desma_pluvio_clima.to_csv('../../data/formatados/dados-pluviometricos-desmatamento-clima.csv', index=False)