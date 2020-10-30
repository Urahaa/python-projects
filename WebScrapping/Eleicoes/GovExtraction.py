#Bibliotecas utilizadas para fazer o web scrapping
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Unica diferença na URL é um código identificando a pagina, criando a lista abaixo poderá ser iterado facilmente
cod_url = ['GI', 'FE', 'EC', 'Genero', 'Situacao']

#Caso a requisição seja bem sucedida atribui-se a response para uma variavel
#Com o BeautifulSoup é realizado o parse do html atribuido a variavel content
#Realizo o cast para string, pois a table é um objeto do tipo BeautifulSoup
#Utilizo o pandas para ler o html e carregar os dados em um dataframe
map_tables = {}
for cod in cod_url:
    req = requests.get('http://apps.tre-sc.jus.br/site/fileadmin/arquivos/eleicoes/estatistica_eleitoral/estat_offline/PerfilEleitor/Munic' + cod +'/PerfilMunic' + cod + '010820.htm')
    if req.status_code == 200:
        content = req.content
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(name='table', attrs={'class':'appDataTable'})
        table_str = str(table)
        dataFrame = pd.read_html(table_str)
        map_tables[cod] = (dataFrame)

#Exportando dados para csv utilitzando o 'to_csv' do pandas
for cod in cod_url:
    info = map_tables.get(cod)
    for i in info:
        i.to_csv(cod + '.csv', sep = ';', encoding='utf-8-sig')
               
        
