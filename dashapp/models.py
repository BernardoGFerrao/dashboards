from dashapp import database, login_manager
from flask_login import UserMixin #Classe que usamos para criação de tabelas

@login_manager.user_loader#Decorator
def load_usuario(id_usuario):#Função: Recebe um id de um usuário e devolve o usuário
    usuario = Usuario.query.get(int(id_usuario))#Busca de usuário
    return usuario


#CRIAÇÃO DAS TABELAS DO BANCO DE DADOS
class Usuario(database.Model, UserMixin): #UserMixin -> é uma classe que implementa métodos e atributos comuns necessários para gerenciar usuários em um sistema web, como login, logout, recuperação de senha, entre outros.
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)