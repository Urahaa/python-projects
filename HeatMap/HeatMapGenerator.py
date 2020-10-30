import pandas as pd
import googlemaps
import gmaps

from GovExtraction import extractGovData
from GoogleGeocodingApi import getLocationByPostalCode
from ipywidgets.embed import embed_minimal_html

API_KEY  = "AIzaSyB8xoaQ2tvLexzFIPbJQ0ttEHNCn1JYoHw"
locations = {}
locations['lat'] = []
locations['lng'] = []
total = []

def getLocationInfo():
    #Recupera os dados do site de eleitores na cidade de blumenau
    dataframe = extractGovData()
    addresses = dataframe['Endereço']
    postalCodes = dataframe['CEP']
    counts = dataframe['Total de Eleitores']
    for address, postalCode, count in zip(addresses, postalCodes, counts):
        #Através da API da google é recuperado a latitude e a longitude passando cep e endereço
        location = getLocationByPostalCode(str(postalCode) + ',' + address)
        locations['lat'].append(location.get('lat'))
        locations['lng'].append(location.get('lng'))
        total.append(count)

def drawHeatMap(zoom, intensity, radius):
    #Configuração da API do google
    gm = googlemaps.Client(key=API_KEY)
    gmaps.configure(api_key=API_KEY)
    #Utilizando o googlemaps é definido a visualização inicial do mapa de calor
    geocode_result = gm.geocode('Blumenau')[0]
    #Gera o mapa de calor a partir da latitude, longitude e a quantidade utilizando o gmaps
    center_lat=geocode_result['geometry']['location']['lat']
    center_lng=geocode_result['geometry']['location']['lng']
    heatmap_layer = gmaps.heatmap_layer(pd.DataFrame(locations), pd.DataFrame(total), dissipating = True)
    heatmap_layer.max_intensity = intensity
    heatmap_layer.point_radius = radius
    fig = gmaps.figure()
    fig = gmaps.figure(center = [center_lat,center_lng], zoom_level=zoom)
    fig.add_layer(heatmap_layer)
    #Exporta o mapa para um html, onde ao acessar é possível realzar o download em png
    embed_minimal_html('c:/temp/export.html', views=[fig])

def main():
    #Popular informações dos eleitores
    getLocationInfo()
    #Gerar o mapa de calor
    drawHeatMap(10, 5, 15)
    
if __name__ == "__main__":
    main()