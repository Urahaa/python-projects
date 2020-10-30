import requests
import json

from types import SimpleNamespace

API_KEY  = "<SUA_API_KEY>"

def getLocationByPostalCode(address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
       'key': API_KEY,
       'address': address,
    }
    req = requests.get(endpoint, params=params)

    if req.status_code == 200:
        address = json.loads(req.content)
        return address.get('results')[0].get('geometry').get('location')
