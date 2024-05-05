#2.Dash:
#Framework que serve para criarmos dashboardas em python, foi construido usando principalmente:
# - plotly -> Gráficos
# - Flask  -> Aplicação


#https://dash.plotly.com/layout

#Como funciona o 2.Dash:
    #Layout: O que aparece na tela
    #  - HTML
    #  - 2.Dash Components(Core Components)
    #Callback: Lógica que comanda o que acontece

#CÓDIGO PADRÃO:
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import openpyxl
import dash_auth

USUARIOS = {
    "Bernardo" : "123",
    "Rafael" : "456"
}

#Criando o aplicativo 2.Dash
app = Dash(__name__)
auth = dash_auth.BasicAuth(app, USUARIOS)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

#Base de dados
df = pd.read_excel(r'D:\GitHub\Bi\Vendas.xlsx')
#Gráfico criado de acordo com o Plotly:
fig1 = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
#https://plotly.com
fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
marcas = list(df['Marca'].unique())
marcas.append('Todas')

lista_paises = list(df["País"].unique())
lista_paises.append("Todos")

#LAYOUT
app.layout = html.Div(children=[
    html.H1(children='Meu Dashboard'),

    html.Div(children='''
        Dashboard de Vendas em Python
    '''),

    html.H3(children="Vendas de cada Produto por Loja", id="subtitulo"),

    dcc.RadioItems(options=marcas, value="Todas", id='selecao_marcas'),
    html.Div(children=[
        dcc.Dropdown(options=lista_paises, value="Todos", id='selecao_pais'),
    ], style={"width": "50%", "margin": "auto"}),

    dcc.Graph(id='vendas_por_loja', figure=fig1),
    dcc.Graph(id='distribuicao_vendas', figure=fig2),

], style={"text-align": "center"})




#CALLBACKS
@app.callback(#Tirar a opção dos botões caso não tenha a marca no país
    Output('selecao_pais', 'options'),
    Input('selecao_marcas', 'value'),
)
def opcoes_pais(marca):
    # criar uma lógica que diga qual a lista de paises que ele vai pegar
    if marca == "Todas":
        nova_lista_paises = list(df["País"].unique())
        nova_lista_paises.append("Todos")
    else:
        df_filtrada = df.loc[df['Marca'] == marca, :]
        nova_lista_paises = list(df_filtrada["País"].unique())
        nova_lista_paises.append("Todos")
    return nova_lista_paises

@app.callback(#Modificar os gráficos!
    Output('subtitulo', 'children'),  # eu quero modificar (eu quero que o botão do input modifique)
    Output('vendas_por_loja', 'figure'),
    Output('distribuicao_vendas', 'figure'),
    Input('selecao_marcas', 'value'),
    # quem está modificando/de onde eu quero pegar a informacao/que tá fazendo um filtro
    Input('selecao_pais', 'value'),
)
def selecionar_marca(marca, pais):
    if marca == "Todas" and pais == "Todos":
        texto = "Vendas de cada Produto por Loja"
        fig1 = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
    else:
        df_filtrada = df
        if marca != "Todas":
            # filtrar de acordo com a marca
            df_filtrada = df_filtrada.loc[df_filtrada['Marca'] == marca, :]
        if pais != "Todos":
            # filtrar de acordo com o pais
            df_filtrada = df_filtrada.loc[df_filtrada["País"] == pais, :]

        texto = f"Vendas de cada Produto por Loja da Marca {marca} e do País {pais}"
        fig1 = px.bar(df_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df_filtrada, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário",
                          size_max=60)
    return texto, fig1, fig2


#Coloca o Dashboard no ar
if __name__ == '__main__':
    app.run(debug=True)