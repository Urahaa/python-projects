#Bibliotecas utilizadas para fazer o web scrapping
import pandas as pd
import requests
from bs4 import BeautifulSoup

def extractGovData():
    req = requests.get('http://apps.tre-sc.jus.br/site/fileadmin/arquivos/eleicoes/estatistica_eleitoral/estat_offline/LocaisVotacao/MunicLocaisVotacao/MunicLocaisVotacao80470.htm')
    if req.status_code == 200:
        dataframe = parseToDataframe(req.content)
        return dataframe

def parseToDataframe(content):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(name='table', attrs={'class':'appDataTable'})
    table_str = str(table)
    dataFrame = pd.read_html(table_str)
    return dataFrame[0]
