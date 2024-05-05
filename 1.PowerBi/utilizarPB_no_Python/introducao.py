# Integração Power BI e Jupyter
# Integrações antigas -> Python dentro do Power BI
# Nova Integração -> Power BI dentro do Python

#BernardoFerraoHashtag716.onmicrosoft.com

#ESSE MÉTODO SÓ FUNCIONA COM POWERBI PRO!!!!

#1.Instalar a biblioteca powerbiclient
#2.Importar Report e models, Autenticação
#3.Realizar a Autenticação
#4.Group_ID e Report_id
#5.Carregar o relatório como group_id e o report_id
#   Pegar essas informações do link do Power BI
#   Precisa ter conta corporativa. Passo a Passo gratuito: https://youtu.be/JCJPD0pRxD8
#   Exemplo de link (não use esse, é só um exemplo): https://app.powerbi.com/groups/61b5c35b-9d17-9e1b0ebd3b5f/reports/82b47b44-b8ed-6b6bade73e24/ReportSection421e7a42c094ea8a1e04
#6.Se der erro para carregar o relatório:
#   Aperte F12
#   Vá em configurações
#   Desative o Javascript source maps e CSS source maps
#   Reinicie o navegador

from powerbiclient import Report, models
from powerbiclient.authentication import DeviceCodeLoginAuthentication

autenticacao = DeviceCodeLoginAuthentication()
# https://app.powerbi.com/groups/me/reports/c7c93e0e-f279-4d6d-94ee-2dff6327e16e/ReportSection421e7a42c094ea8a1e04?redirectedFromSignup=1&experience=power-bi

group_id = 'codigo/arquivo'
report_id = 'codigo/arquivo'

relatorio = Report(group_id=group_id, report_id=report_id, auth=autenticacao)

from IPython.display import IFrame
print(IFrame(src="https://app.powerbi.com/reportEmbed?reportId=d71c6356-b975-4a32-a09a-f173a40539fe&autoAuth=true&ctid=56f958aa-959f-40ce-9f84-8186316b3219&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWJyYXppbC1zb3V0aC1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D", width=1140, height=541))

#### Agora podemor interagir com o relatório
paginas = relatorio.get_pages()
print(len(paginas))

for pagina in paginas:
    print("*" * 10)
    print(pagina)
    if pagina['displayName'] == "Relatório de Vendas":
        relatorio_vendas = pagina

### Vamos puxar agora 1 página: Relatório de Vendas
print(relatorio_vendas)
graficos = relatorio.visuals_on_page(relatorio_vendas['name'])

for grafico in graficos:
    print("*" * 10)
    print(grafico)
    if grafico['type'] == 'barChart':
        grafico_area = grafico


### Pegar os gráficos de área (ou gráfico com determinada condição, como Título)
print(grafico_area)

### Exportar informações do Power BI para o Python
infos_grafico = relatorio.export_visual_data(relatorio_vendas['name'], grafico_area['name'], rows=100)
print(infos_grafico)

import pandas as pd
from io import StringIO
tabela = pd.read_csv(StringIO(infos_grafico))
print(tabela)

### Outra forma de exportar
infos_grafico2 = relatorio.export_visual_data(relatorio_vendas['name'], grafico_area['name'], rows=1000, export_data_type=1)
print(infos_grafico2)

tabela2 = pd.read_csv(StringIO(infos_grafico2))
print(tabela2)

#Trabalhar com Filtros
#Identificar se tem um filtro aplicado:
print(relatorio.get_filters())

def filter_report(Anos):
    anos_filter = {
        '$schema': "http://powerbi.com/product/schema#basic",
        'target': {
            'table': "Calendário",
            'column': "Ano"
        },
        'operator': "In",
        'values': [Anos]
    }
    relatorio.remove_filters()
    relatorio.update_filters([anos_filter])

from ipywidgets import interact
interact(filter_report, Anos=[2016, 2017, 2018])

### Verificar slicers (ainda não funciona)
filtros = []
for visual in relatorio.visuals_on_page(relatorio_vendas['name']):
    if visual['type'] == 'slicer':
        filtros.append(visual)

print(filtros)

for filtro in filtros:
    print(relatorio.export_visual_data(relatorio_vendas['name'], filtro['name'], rows=1000))