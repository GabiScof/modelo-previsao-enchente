import pandas as pd
from pandas import DataFrame

class formataCSV:

    def separa_coluna_data(self,df:DataFrame):

        df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month

        df.drop(columns=['data'], inplace=True)

        return df

    def agrupa_por_mes(self,df:DataFrame):
        df = df.groupby(['ano', 'mes', 'estacao'], as_index=False)['chuva'].mean()
        return df

    def merge_codigo_municipio(self,df_codigos:DataFrame, df_municipios: DataFrame):
        df = pd.merge(
            df_codigos,
            df_municipios,
            left_on='estacao',
            right_on='codigo_estacao',
            how='left'
        )
        return df

if __name__ == "__main__":
    classe = formataCSV()
    df = pd.read_csv('../../data/brutos/dados-pluviometricos-AP.csv')
    df = classe.separa_coluna_data(df=df)
    df = classe.agrupa_por_mes(df=df)
    df.to_csv('../../data/formatados/dados-pluviometricos-AP.csv', index=False)

    df_municipios = pd.read_csv('../../data/brutos/estacao-pluviometrica-municipio.csv')
    df = classe.merge_codigo_municipio(df_codigos=df, df_municipios=df_municipios)
    print(df)
