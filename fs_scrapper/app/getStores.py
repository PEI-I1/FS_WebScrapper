import json
import re
import requests
import os

STORE_URL = 'https://www.nos.pt/particulares/Pages/lojas-nos.aspx/_layouts/15/NOS/StoreSearchService.svc/GetAllStores?listName=Lojas'
FIELDS = ['Title', 'Street', 'Schedule', 'Locality', 'StoreLatitude', 'StoreLongitude', 'District', 'TownHall', 'AvailableServices']
FIELDSPT = ['nome', 'morada', 'horario', 'localidade', 'latitude', 'longitude', 'distrito', 'concelho', 'listaservs']

def mapToPT(field):
    i = 0
    while field != FIELDS[i]:
        i = i + 1

    return FIELDSPT[i]

def crawlStores():
    """ Dumps store data from NOS endpoint
    """
    resp = requests.post(STORE_URL)
    if resp.status_code == 200:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/../json/stores_raw.json", "w", encoding='utf8') as store_raw_dump:
            stores_raw = json.loads(resp.json())
            json.dump(stores_raw, store_raw_dump, indent=4, ensure_ascii=False)
        return True
    else:
        return False

def cleanJson():
    """ Loads json and extracts fields of interest
    """
    stores_proc = []
    with open(os.path.dirname(os.path.abspath(__file__)) + "/../json/stores_raw.json", "r") as store_raw_dump:
        stores_raw = json.load(store_raw_dump)

    for store in stores_raw:
        tmp = {}
        for field in FIELDS:
            if field != 'AvailableServices':
                aux = re.sub(r'(</br>)+', ' ', store[field])
                aux = re.sub(r'^\s+', '', aux)
                tmp[mapToPT(field)] = re.sub(r'\s+$', '', aux)
            else:
                i = 0
                dic = []
                while i < len(store[field]):
                    dic.append(store[field][i]['Title'])
                    i = i+1

                tmp[mapToPT(field)] = dic

        stores_proc.append(tmp)

    with open(os.path.dirname(os.path.abspath(__file__)) + "/../json/lojas.json", "w", encoding='utf8') as store_dump:
        json.dump(stores_proc, store_dump, indent=4, ensure_ascii=False)

def update_lojas():
    if crawlStores():
        cleanJson()
        os.remove(os.path.dirname(os.path.abspath(__file__)) + '/../json/stores_raw.json')
