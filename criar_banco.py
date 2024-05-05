from dashapp import server, database
from dashapp.models import Usuario #Importa a tabela usuario

with server.app_context():#Código padrão
    database.create_all()#Cria todo o db