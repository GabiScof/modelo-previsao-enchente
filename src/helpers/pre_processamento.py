import pandas as pd
import unicodedata
from pandas import DataFrame

class PreProcessamento:
    def preenche_com_media(self, df:DataFrame, coluna: str):
        medias = (
            df.dropna(subset=[coluna])  # ignora linhas onde chuva é NaN
            .groupby(['ano', 'mes', 'municipio'])[coluna]
            .mean()
            .reset_index()
            .rename(columns={coluna: coluna+'_media'})
        )
        return medias
