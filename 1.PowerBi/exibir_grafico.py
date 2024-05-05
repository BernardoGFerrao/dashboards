#visualizações -> PY
#Editor de scripts python:

#Dentro do Bi -> Transformar dados:
import pandas as pd
import os
from tabulate import tabulate

#importando os arquivos
caminho_padrao = r'D:\GitHub\Bi'
vendas_df = pd.read_csv(os.path.join(caminho_padrao, r'Contoso - Vendas - 2017.csv'), sep=';', encoding='cp1252')
produtos_df = pd.read_csv(os.path.join(caminho_padrao, r'Contoso - Cadastro Produtos.csv'), sep=';', encoding='cp1252')
lojas_df = pd.read_csv(os.path.join(caminho_padrao, r'Contoso - Lojas.csv'), sep=';', encoding='cp1252')
clientes_df = pd.read_csv(os.path.join(caminho_padrao, r'Contoso - Clientes.csv'), sep=';', encoding='cp1252')

# Substituir o caractere ÿ por i em todos os DataFrames
dfs = [vendas_df, produtos_df, lojas_df, clientes_df]
for df in dfs:
    df.columns = df.columns.str.replace('ÿ', '')

#limpando apenas as colunas que queremos
clientes_df = clientes_df[['ID Cliente', 'E-mail']]
produtos_df = produtos_df[['ID Produto', 'Categoria']]
lojas_df = lojas_df[['ID Loja', 'Nome da Loja']]

#mesclando e renomeando os dataframes
vendas_df = vendas_df.merge(produtos_df, on='ID Produto')
vendas_df = vendas_df.merge(lojas_df, on='ID Loja')
vendas_df = vendas_df.merge(clientes_df, on='ID Cliente').rename(columns={'E-mail': 'E-mail do Cliente'})
# print(vendas_df)

#EDIÇÃO -> Filtro da tabela anterior
dataset = vendas_df
tres_lojas_df = dataset[dataset['ID Loja'].isin([86, 306, 72])]
#Caso desse problema com as datas -> Transformar em texto no power bi
#Fechar e aplicar

#PLOTAR:
import matplotlib.pyplot as plt
tres_lojas_df.plot(x='Data da Venda', y='Quantidade Vendida', figsize=(15, 5))
plt.show()