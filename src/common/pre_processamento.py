import pandas as pd

from src.helpers.formata_csv import formataCSV
from src.helpers.desmatamento import Desmatamento
from src.helpers.formata_csv_clima import formataCSVClima


if __name__ == "__main__":
    classe = formataCSV()
    desmatamento = Desmatamento()

    # Leitura dos dataframe de pluviometria, municipio e desmatamento
    df_ap = pd.read_csv('../../data/brutos/dados-pluviometricos-AP.csv')
    df_ac = pd.read_csv('../../data/brutos/dados-pluviometricos-AC.csv')
    df_ma = pd.read_csv('../../data/brutos/dados-pluviometricos-MA.csv')
    df_ro = pd.read_csv('../../data/brutos/dados-pluviometricos-RO.csv')
    df_rr = pd.read_csv('../../data/brutos/dados-pluviometricos-RR.csv')
    df_vazao_ac = pd.read_csv('../../data/brutos/dados-vazao-AC.csv')
    df_vazao_am = pd.read_csv('../../data/brutos/dados-vazao-AM.csv')
    df_vazao_ap = pd.read_csv('../../data/brutos/dados-vazao-AP.csv')
    df_vazao_ma = pd.read_csv('../../data/brutos/dados-vazao-MA.csv')
    df_vazao_mt = pd.read_csv('../../data/brutos/dados-vazao-MT.csv')
    df_vazao_pa = pd.read_csv('../../data/brutos/dados-vazao-PA.csv')
    df_vazao_ro = pd.read_csv('../../data/brutos/dados-vazao-RO.csv')
    df_vazao_rr = pd.read_csv('../../data/brutos/dados-vazao-RR.csv')
    df_vazao_to = pd.read_csv('../../data/brutos/dados-vazao-TO.csv')
    df_municipios = pd.read_csv('../../data/brutos/estacao-pluviometrica-municipio.csv')
    df_municipios_vazao = pd.read_csv('../../data/brutos/estacao-vazao-municipio.csv')
    df_desmatamento= pd.read_csv('../../data/brutos/desmatamento_por_municipio.csv')
    df_desmatamento_datazoom= pd.read_csv('../../data/brutos/mapbiomas_muni_deforestation_regeneration.csv',  sep=';')
    df_clima = pd.read_csv('../../data/extracao/dados-clima-final.csv', encoding='latin1', sep=';', engine='python')

    #df_desmatamento_datazoom = df_desmatamento_datazoom[['municipio','uf','cod_municipio','ano','valor','classe_desmatamento']]
    #df_desmatamento_datazoom = df_desmatamento_datazoom[df_desmatamento_datazoom['classe_desmatamento'].str.contains('Supressao')]

    # DADOS DE PLUVIOMETRIA -----------------------------------------------------------------------------------
    # Criação do dataframe de pluviometria com todos os estados
    lista_dfs = [df_ap,df_ac, df_ma, df_ro,df_rr]
    df_pluviometria = classe.concatena_df(lista_dfs=lista_dfs)

    # Pré-processamento de colunas
    df_pluviometria = classe.separa_coluna_data(df=df_pluviometria)
    df_pluviometria = classe.agrupa_por_mes(df=df_pluviometria, coluna='chuva')

    # Agrupamento dos dataframes de código de município e nome de município
    df_pluviometria = classe.merge_codigo_municipio(df_codigos=df_pluviometria, df_municipios=df_municipios)

    # DADOS DE VAZÃO -----------------------------------------------------------------------------------
    # Criação do dataframe de pluviometria com todos os estados
    lista_dfs_vazao = [df_vazao_am,df_vazao_ac,df_vazao_mt,df_vazao_ap,df_vazao_ma,df_vazao_ro,df_vazao_rr,df_vazao_pa,df_vazao_to]
    df_vazao = classe.concatena_df(lista_dfs=lista_dfs_vazao)

    # Pré-processamento de colunas
    df_vazao = classe.separa_coluna_data(df=df_vazao)
    df_vazao = classe.agrupa_por_mes(df=df_vazao, coluna='vazao')

    # Agrupamento dos dataframes de código de município e nome de município
    df_vazao = classe.merge_codigo_municipio(df_codigos=df_vazao, df_municipios=df_municipios_vazao)

    # TODOS OS DATAFRAMES -----------------------------------------------------------------------------------
    # Pré-processamento de strings
    df_pluviometria['municipio'] = df_pluviometria['municipio'].apply(classe.formata_string)
    df_desmatamento['municipality'] = df_desmatamento['municipality'].apply(classe.formata_string)
    #df_desmatamento_datazoom['municipio'] = df_desmatamento_datazoom['municipio'].astype(str)
    df_vazao['municipio'] = df_vazao['municipio'].apply(classe.formata_string)
    df_clima['municipio'] = df_clima['municipio'].apply(classe.formata_string)

    # Seleção das colunas do df de desmatamento
    df_desmatamento = df_desmatamento[['year', 'areakm', 'municipality']]
    df_desmatamento_datazoom = df_desmatamento_datazoom[['municipio','uf','cod_municipio','ano','valor','classe_desmatamento']]

    # Renomeação das colunas do df de desmatamento
    df_desmatamento.rename(columns={'year': 'ano', 'municipality': 'municipio'}, inplace=True)

    # Calculo de desmatamento do dataframe do datazoom
    df_desmatamento_datazoom = df_desmatamento_datazoom[df_desmatamento_datazoom['classe_desmatamento'].str.contains('Supressao')]
    df_desmatamento_datazoom = df_desmatamento_datazoom[df_desmatamento_datazoom['ano'] >= 1991]
    df_desmatamento_datazoom['municipio'] = df_desmatamento_datazoom['municipio'].apply(classe.formata_string)
    df_desmatamento_datazoom['valor'] = df_desmatamento_datazoom['valor'].astype(str).str.replace(',', '.').astype(float)
    df_desmatamento_datazoom = df_desmatamento_datazoom.groupby(['ano', 'municipio'])['valor'].sum().reset_index()
    df_desmatamento_datazoom['valor'] = df_desmatamento_datazoom['valor'] / 100

    # Agrupamento dos dataframes de pluviometria, desmatamento e vazão
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df_pluviometria, df_desmatamento=df_desmatamento, condicoes=['ano', 'municipio'], modo = 'left')
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df_desma_pluvio, df_desmatamento=df_desmatamento_datazoom, condicoes=['ano', 'municipio'], modo = 'left')
    df_desma_pluvio_vazao = classe.agrupa_csv(df_pluviometria=df_desma_pluvio, df_desmatamento=df_vazao, condicoes=['ano', 'mes', 'municipio'], modo = 'outer')

    # Preenchimento dos valores de desmatamento nan do dataframe destamamento com o dataframe desmatamento do datazoom
    df_desma_pluvio_vazao['areakm'] = df_desma_pluvio_vazao['areakm'].fillna(df_desma_pluvio_vazao['valor'])

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
    df_desma_pluvio_vazao_clima = classe.agrupa_csv(df_pluviometria=df_desma_pluvio_vazao, df_desmatamento=df_clima, condicoes=['ano', 'mes', 'municipio'], modo='left')
    df_desma_pluvio_vazao_clima['chuva_final'] = df_desma_pluvio_vazao_clima['precipitacao_total_mm'].combine_first(df_desma_pluvio_vazao_clima['chuva'])

    # Retirar colunas desnecessárias
    df_desma_pluvio_vazao_clima = df_desma_pluvio_vazao_clima.drop(columns = ['estacao_y', 'codigo_estacao_y', 'estacao_x', 'codigo_estacao_x', 'chuva', 'precipitacao_total_mm'])
    df_desma_pluvio_vazao_clima.rename(columns={'uf_x': 'uf'})


    # Exportação dos csv de pluviometria e desmatamento
    df_pluviometria.to_csv('../../data/formatados/dados-pluviometricos.csv', index=False)
    df_desma_pluvio.to_csv('../../data/formatados/dados-pluviometricos-desmatamento.csv', index=False)
    df_desma_pluvio_vazao_clima.to_csv('../../data/formatados/dados-pluviometricos-vazao-desmatamento-clima.csv', index=False)