import pandas as pd

from src.helpers.pre_processamento import PreProcessamento

if __name__ == "__main__":
    preprocessamento = PreProcessamento()
    df = pd.read_csv('../../data/formatados/dados-pluviometricos-vazao-desmatamento-clima.csv')

    medias = preprocessamento.preenche_com_media(df=df, coluna = 'chuva_final')
    df = pd.merge(df, medias, on=['ano', 'mes', 'municipio'], how='left')

    medias = preprocessamento.preenche_com_media(df=df, coluna = 'vazao')
    df = pd.merge(df, medias, on=['ano', 'mes', 'municipio'], how='left')

    df = df.drop_duplicates(subset=['ano', 'mes', 'municipio'])

    df.drop(columns=['chuva_final', 'vazao'], inplace=True)

    print('teste')
