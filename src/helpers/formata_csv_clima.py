import pandas as pd
from pandas import DataFrame

class formataCSVClima:

    def separa_coluna_dia_mes_ano(self,df:DataFrame):
        nome_primeira_coluna = df.columns[0]

        df['data'] = pd.to_datetime(df[nome_primeira_coluna], format='%Y-%m-%d', errors='coerce')
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month
        df['dia'] = df['data'].dt.day

        df.drop(columns=['data', nome_primeira_coluna], inplace=True)

        return df

    def agrupa_por_mes(self,df:DataFrame):
        df.drop(columns=['dia'], inplace=True)
        colunas = df.columns.tolist()
        colunas = [col for col in colunas if col not in ['ano', 'mes', 'estado', 'municipio']]
        df = df.groupby(['ano', 'mes', 'estado', 'municipio'], as_index=False)[colunas].mean(numeric_only=True)
        return df

    def remover_valores_invalidos(self, df: DataFrame, coluna: str):
        df = df[df[coluna].notna()]
        df = df[~df[coluna].astype(str).str.strip().eq('')]
        df = df[~df[coluna].astype(str).str.strip().eq('-9999')]

        return df

    def transforma_numerico(self, df:DataFrame, colunas_numericas : list):
        for col in colunas_numericas:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
