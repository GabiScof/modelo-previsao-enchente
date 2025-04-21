import pandas as pd

from src.helpers.formata_csv import formataCSV

if __name__ == "__main__":
    classe = formataCSV()

    # Leitura dos dataframe de pluviometria, municipio e desmatamento
    df = pd.read_csv('../../data/brutos/dados-pluviometricos-AP.csv')
    df_municipios = pd.read_csv('../../data/brutos/estacao-pluviometrica-municipio.csv')
    df_desmatamento= pd.read_csv('../../data/brutos/desmatamento_por_municipio.csv')

    # Pré-processamento de colunas
    df = classe.separa_coluna_data(df=df)
    df = classe.agrupa_por_mes(df=df)

    # Agrupamento dos dataframes de código de município e nome de município
    df = classe.merge_codigo_municipio(df_codigos=df, df_municipios=df_municipios)

    # Pré-processamento de strings
    df['municipio'] = df['municipio'].apply(classe.formata_string)
    df_desmatamento['municipality'] = df_desmatamento['municipality'].apply(classe.formata_string)

    # Seleção das colunas do df de desmatamento
    df_desmatamento = df_desmatamento[['year', 'areakm', 'municipality']]

    # Renomeação das colunas do df de desmatamento
    df_desmatamento.rename(columns={'year': 'ano', 'municipality': 'municipio'}, inplace=True)

    # Agrupamento dos dataframes de pluviometria e desmatamento
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df, df_desmatamento=df_desmatamento)

    # Exportação dos csv de pluviometria e desmatamento
    df.to_csv('../../data/formatados/dados-pluviometricos-AP.csv', index=False)
    df_desma_pluvio.to_csv('../../data/formatados/dados-pluviometricos-desmatamento.csv', index=False)
