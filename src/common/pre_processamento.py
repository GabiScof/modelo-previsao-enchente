import pandas as pd

from src.helpers.formata_csv import formataCSV

if __name__ == "__main__":
    classe = formataCSV()

    # Leitura dos dataframe de pluviometria, municipio e desmatamento
    df_ap = pd.read_csv('../../data/brutos/dados-pluviometricos-AP.csv')
    df_ac = pd.read_csv('../../data/brutos/dados-pluviometricos-AC.csv')
    df_municipios = pd.read_csv('../../data/brutos/estacao-pluviometrica-municipio.csv')
    df_desmatamento= pd.read_csv('../../data/brutos/desmatamento_por_municipio.csv')

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
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df_pluviometria, df_desmatamento=df_desmatamento)

    # Exportação dos csv de pluviometria e desmatamento
    df_pluviometria.to_csv('../../data/formatados/dados-pluviometricos.csv', index=False)
    df_desma_pluvio.to_csv('../../data/formatados/dados-pluviometricos-desmatamento.csv', index=False)
