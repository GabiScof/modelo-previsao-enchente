import pandas as pd
import unicodedata
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

    def agrupa_csv(self,df_pluviometria:DataFrame, df_desmatamento: DataFrame):

        df = pd.merge(
            df_pluviometria,
            df_desmatamento,
            on=['ano', 'municipio'],
            how='left'
        )
        return df

    def formata_string(self, string: str):
        if isinstance(string, str):
            string = str(string).strip().lower()
            string = unicodedata.normalize('NFD', string)
            string = ''.join(c for c in string if unicodedata.category(c) != 'Mn')  # Remove acentos
        return string
