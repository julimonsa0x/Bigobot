import json
import urllib.request

from functions import printt

def covid_api_request(endpoint):
    try:
        covid_request_url = urllib.request.Request('https://api.covid19api.com/' + endpoint)
        covid_request_data = json.loads(urllib.request.urlopen(covid_request_url).read().decode('utf-8'))
        return covid_request_data
    except Exception as e:
        printt(f"====| Ocurrio un error al pedir los datos de la api covid19.\nDetalles:{e}\nRazon:{e.args}")