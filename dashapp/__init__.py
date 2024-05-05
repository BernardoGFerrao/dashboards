from dash import Dash
#from flask import flask
from flask_login import LoginManager #Gerencia a autenticação
from flask_bcrypt import Bcrypt#Cria a criptografia
from flask_sqlalchemy import SQLAlchemy#Banco de dados


#app = Flask(__name__) porém é sobescrito pelo 2.Dash:
app = Dash(__name__)

#Cria o servidor do flask:
server = app.server

#Desativa as exceções de outras telas
app.config.suppress_callback_exceptions = True

#Configuração do servidor:
server.config.update(
    SQLALCHEMY_DATABASE_URI="sqlite:///bancodedados.db",  #Link banco de dados
    SECRET_KEY="f7s8gsh6f5s5fsg5sfg7s5gs65g1k90128jsudh", #Chave que o flasklogin usa para configurar a segurança do site
    SQLALCHEMY_TRACK_MODIFICATIONS=False,                 #Não analisa todas modificações do servidor
)

#Criações:
#DB
database = SQLAlchemy(server)
#Criptografador
bcrypt = Bcrypt(server)
#Gerenciador de login
login_manager = LoginManager(server)
login_manager.login_view = "/login"#Definimos os caminhos do site

from dashapp import views