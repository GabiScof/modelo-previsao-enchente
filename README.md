# Modelo de Previsão de Enchentes 
Criação de um modelo de previsão para determinar em quais datas futuras haverá enchente na região da Floresta Amazônica
<br><br>

## Fonte dos Dados

Os dados extraídos estão localizados em `data/brutos` :
<br><br>

1. **Dados pluviométricos por município e estado** 

Representam a quantidade de chuva registrada por dia e mês em municípios dos respectivos estados entre os anos 1991 e 2024.
- `dados-pluviometricos-AC.csv`
- `dados-pluviometricos-AP.csv`

**FONTE**: API Hidro Webservice do ANA 

Para ver como os dados foram extraídos, consulte o github : 🔗 (https://github.com/GabiScof/modelo-previsao-enchentes)
<br><br>

2. **Dados de desmatamento por município e estado** 

Representam a quantidade área desmatada por mês em municípios dos respectivos estados entre os anos 2007 e 2024.
- `desmatamento_por_municipio.csv`

**FONTE**: 🔗 [Terra Brasilis](https://terrabrasilis.dpi.inpe.br/app/dashboard/deforestation/biomes/legal_amazon/increments)
<br><br>

3. **Dados de códigos de estação associados a município** 

Associa o código de uma estação pluviométrica a seu respectivo município.
- `estacao-pluviometrica-municipio.csv`

**FONTE**: API Hidro Webservice do ANA 

Para ver como os dados foram extraídos, consulte o github : 🔗 (https://github.com/GabiScof/modelo-previsao-enchentes)
<br><br>
