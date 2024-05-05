from dash import html, dcc, Input, Output, State
from dashapp import app, server, database, bcrypt
from dashapp.models import Usuario
from flask_login import login_user, logout_user, current_user#IMPEDE O USUÁRIO DE ACESSAR AS PÁGINAS SEM ESTAR LOGADO

opcoes_dropdown = [
    {"label": "Dia 1", "value": "Dia 1"},
    {"label": "Dia 2", "value": "Dia 2"}
]

#LAYOUTS das páginas/telas:
layout_homepage = html.Div([
    dcc.Location(id="homepage_url", refresh=True),#Passa o Pathname para o callback
    html.H2("Criar conta"),
    html.Div([
        dcc.Input(id="email", type="email", placeholder="Seu e-mail"),
        dcc.Input(id="senha", type="password", placeholder="Sua senha"),
        html.Button("Criar conta", id="botao-criarconta"),
        dcc.Link("Já tem uma conta? Faça seu login aqui", "/login")#mensagem, página que ele vai
    ], className="form-column")#Faz com que eles fiquem em coluna e com um espaço entre os links
])

layout_login = html.Div([
    dcc.Location(id="login_url", refresh=True),#Passa o Pathname para o callback
    html.H2("Faça seu Login"),
    html.Div([
        dcc.Input(id="email", type="email", placeholder="Seu e-mail"),
        dcc.Input(id="senha", type="password", placeholder="Sua senha"),
        html.Button("Faça Login", id="botao-login"),
        dcc.Link("Não tem uma conta? Crie aqui", "/")#mensagem, página que ele vai
    ], className="form-column")#Faz com que eles fiquem em coluna e com um espaço entre os links
])

layout_dashboard = html.Div([
    dcc.Location(id="dashboard_url", refresh=True),#Passa o Pathname para o callback
    html.H2("Meu Dashboard"),
    dcc.Dropdown(id="dropdown", options=opcoes_dropdown, value="Dia 1"),
    dcc.Graph(id="grafico"),
])

layout_erro = html.Div([
    dcc.Location(id="erro_url", refresh=True),#Passa o Pathname para o callback
    html.H2("Erro de Acesso"),
    html.Div([
        dcc.Link("Clique aqui para criar uma conta", "/"),#mensagem, página que ele vai
        dcc.Link("Clique aqui para fazer login", "/login")#mensagem, página que ele vai
    ], className="form-column")#Faz com que eles fiquem em coluna e com um espaço entre os links
])

#LAYOUT GERAL(Recebe os outros layouts através do callback):
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),#Passa o Pathname para o callback
    html.Div([
        html.H1("Dashapp"),
        html.Div(id="navbar"),
    ], className="align-left-right"),
    html.Div(id="conteudo_pagina")#DIV QUE VAI SER EDITADA!!!
])


#EDITA O CONTEUDO_PÁGINA de acordo o link
@app.callback(Output("conteudo_pagina", "children"), Input("url", "pathname"))
def carregar_pagina(pathname):
    if pathname == "/":
        return layout_homepage
    elif pathname == "/dashboard":
        if current_user.is_authenticated:
            return layout_dashboard
        else:
            return dcc.Link("Usuario não autenticado, faça login aqui", "/login")
    elif pathname == "/login":
        return layout_login
    elif pathname == "/erro":
        return layout_erro
    elif pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
        return layout_login

#CONTROLA A BARRA DE NAVEGAÇÃO
@app.callback(Output("navbar", "children"), Input("url", "pathname"))
def exibir_navbar(pathname):
    if pathname != "/logout":
        if current_user.is_authenticated:
            return html.Div([
                dcc.Link("Dashboard", "/dashboard", className="button-link"),
                dcc.Link("Logout", "/logout", className="button-link")
            ])
        else:
            return html.Div([
                dcc.Link("Login", "/login", className="button-link")
            ])

#FUNCIONALIDADE DE CRIAR CONTA:
@app.callback(Output("homepage_url", "pathname"), Input("botao-criarconta", "n_clicks"), 
              [State("email", "value"), State("senha", "value")])
def criar_conta(n_clicks, email, senha):#N clicks nos diz se o usuário clicou no botão
    if n_clicks:
        # vou criar a conta
        # verificar se já existe um usuário com essa conta
        usuario  = Usuario.query.filter_by(email=email).first() # finalizar
        if usuario:
            return "/login"
        else:
            # criar o usuario
            #Criptografa a senha:
            senha_criptografada = bcrypt.generate_password_hash(senha).decode("utf-8")
            # Adiciona o usuário
            usuario = Usuario(email=email, senha=senha_criptografada)
            database.session.add(usuario)
            database.session.commit()
            #Faz o login do usuário
            login_user(usuario)
            return "/dashboard"

#VAI FAZER LOGIN
@app.callback(Output("login_url", "pathname"), Input("botao-login", "n_clicks"), #Input -> Start o callback
              [State("email", "value"), State("senha", "value")])#STATE -> Variável que podemos extrair alguma informação dentro da página
def criar_conta(n_clicks, email, senha):#N clicks nos diz se o usuário clicou no botão
    if n_clicks:
        # vou criar a conta
        # verificar se já existe um usuário com essa conta
        usuario = Usuario.query.filter_by(email=email).first() #Busca o usuário através do email no DB
        if not usuario:
            return "/"
        else:
            if bcrypt.check_password_hash(usuario.senha.encode("utf-8"), senha): #Verifica se a senha digitada esta correta
                login_user(usuario)#faz login
                return "/dashboard"
            else:
                return "/erro"


#EDITA O CONTEUDO DO GRÁFICO DE ACORDO COM O DROPDOWN
@app.callback(Output("grafico", "figure"), Input("dropdown", "value"))
def atualizar_grafico(valor_dropdown):
    if valor_dropdown == "Dia 1":
        pontos = {"x": [1, 2, 3, 4], "y": [4, 1, 2, 1]}
        titulo = "Gráfico Dia 1"
    else:
        pontos = {"x": [1, 2, 3, 4], "y": [2, 3, 2, 4]}
        titulo = "Gráfico Dia 2"
    return {"layout": {"title": titulo}, "data": [pontos]}



#----- TELAS -----:
#FLASK:
#@app.route("/nova_tela")
#def
#DASH:
@server.route("/nova_tela")
def nova_tela():
    return "Você está na página criada pelo Flask"
