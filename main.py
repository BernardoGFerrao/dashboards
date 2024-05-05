#Como a pasta dashapp possui um init, podemos importar:
from dashapp import app
#Esse if faz com que o código dentro só rode, caso o main seja rodado, e não caso seja importado
if __name__ == "__main__":
    app.run_server(debug=True)