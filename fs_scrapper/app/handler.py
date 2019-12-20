import json
from re import sub
from haversine import haversine, Unit


def linhas_apoio():
    """ Retrieve service lines
    """
    with open('json/linhas_apoio.json', 'r') as f:
        data = json.load(f)
        lista = []

        for linha in data:
            lista.append(linha)

        return lista


def linhas_apoio_assunto(assunto):
    """ Retrieve the service line following a specific matter
    :param: matter
    """
    with open('json/linhas_apoio.json', 'r') as f:
        data = json.load(f)
        lista = []

        for linha in data:
            if linha['categoria'].lower() == assunto.lower():
                lista.append(linha)
                return lista

            elif assunto.lower() in linha['categoria'].lower():
                lista.append(linha)

        return lista


def all_phones():
    """ Retrieve all phones available
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            aux['nome'] = phone['nome']
            aux['preco'] = phone['preço']
            aux['tags'] = phone['tags']
            aux['link'] = phone['link']
            aux['pretacoes'] = phone['prestações']
            aux['pontos'] = phone['pontos']
            lista.append(aux)
            aux = {}

        return lista


def brand_phones(marca, phones):
    """ Retrieve all phones of specified brand
    :param: brand
    :param: list of phones
    """
    lista = []

    for phone in phones:
        if marca.lower() in phone['nome'].lower():
            lista.append(phone)

    return lista


def top_phones(phones):
    """ Retrive the top most shearched/viewed phones
    :param: list of phones
    """
    with open('json/top_phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        
        for phone in phones:
            for top in data:
                if phone['nome'] == top['nome']:
                    lista.append(phone)

        return lista


def promo_phones(phones):
    """ Retrieve all phones who are currently under a discount/promotion
    :param: list of phones
    """
    lista = []

    for phone in phones:
        if 'desconto' in phone['tags']:
            lista.append(phone)

    return lista


def new_phones(phones):
    """ Retrieve the most recents phones
    :param: list of phones
    """
    lista = []

    for phone in phones:
        if 'novidade' in phone['tags']:
            lista.append(phone)

    return lista


def ofer_phones(phones):
    """ Retrieve all the phones in which it comes with an offer
    :param: list of phones
    """
    lista = []

    for phone in phones:
        for tag in phone['tags']:
            if 'oferta' in tag:
                lista.append(phone)

    return lista


def prest_phones(phones):
    """ Retrieve all phones which have installment payment avaiable
    :param: list of phones
    """
    lista = []

    for phone in phones:
        if phone['prestações'] == 'Disponível':
            lista.append(phone)

    return lista


def points_phones(phones):
    """ Retrieve all phones which have points payment avaiable
    :param: list of phones
    """
    lista = []

    for phone in phones:
        if phone['pontos'] == 'Disponível':
            lista.append(phone)

    return lista

def str_to_float(value):
    value = sub(r'[^\d,.]', '', value)
    value = sub(r',', '.', value)
    ret = float(value)
    return ret

def phones_by_price(inf, sup, phones):
    """ Retrieve all phones which are in specified threshold of price
    :param: lowest number of price
    :param: highest number of price
    :param: list of phones
    """
    lista = []
    
    inf = str_to_float(inf)
    sup = str_to_float(sup)

    for phone in phones:
        preco = str_to_float(phone['preco'])

        if inf <= preco <= sup:
            lista.append(phone)

    return lista


def all_wtf():
    """ Retrieve all 'WTF' tariffs avaiable
    """
    with open('json/tarifario_WTF.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for tarifario in data:
            aux['nome'] = tarifario['Nome_Tarifario']
            aux['preco'] = tarifario['Preco']
            aux['minutos'] = tarifario['Minutos']
            aux['net'] = tarifario['Net']
            aux['sms'] = tarifario['SMS']
            lista.append(aux)
            aux = {}

        return lista


def wtf_name(nome):
    """ Retrieve information of specified tariff
    :param: tariff name
    """
    with open('json/tarifario_WTF.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for tarifario in data:
            if nome.lower() in tarifario['Nome_Tarifario'].lower():
                aux['nome'] = tarifario['Nome_Tarifario']
                aux['preco'] = tarifario['Preco']
                aux['preco_total'] = tarifario['Preco_Total']
                aux['minutos'] = tarifario['Minutos']
                aux['net'] = tarifario['Net']
                aux['sms'] = tarifario['SMS']
                aux['cinema'] = tarifario['Cinema']
                aux['uber'] = tarifario['Uber']
                aux['uber_eats'] = tarifario['Uber_eats']
                lista.append(aux)
                aux = {}

        return lista


def stores_by_zone(zona):
    """ Retrieve the stores avaiable at specified region
    :param: region
    """
    with open('json/lojas.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for loja in data:
            if zona.lower() in loja['morada'].lower() or zona.lower() == loja['localidade']:
                aux['nome'] = loja['nome']
                aux['morada'] = loja['morada']
                aux['horario'] = loja['horario']
                lista.append(aux)
                aux = {}

        return lista


def haversine_distance(c1, c2):
    """ Calculate the distance between two points on a spherical surface
    :param: Point 1
    :param: Point 2
    """
    location_1 = c1
    location_2 = c2
    return haversine(location_1, location_2, unit=Unit.KILOMETERS)


def stores_by_coordinates(lat, lon):
    """ Retrieve the stores avaiable around 20km of the given coordinates
    :param: latitude
    :param: longitude
    """
    with open('json/lojas.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for loja in data:
            distance = haversine_distance((lat,lon),(float(loja['latitude']),float(loja['longitude'])))
            if  distance < 20:
                aux['nome'] = loja['nome']
                aux['morada'] = loja['morada']
                aux['horario'] = loja['horario']
                lista.append(aux)
                aux = {}

        return lista


def specific_package(nome):
    """ Retrieve package of certain type and specific name
    :param: package name
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)
        lista = []

        for pacote in data:
            if nome.lower() in pacote['nome'].lower():
                lista.append(pacote)

        return lista


def packages():
    """ Retrieve all packages avaiable
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for pacote in data:
            aux['tipo'] = pacote['Tipo']
            aux['nome'] = pacote['nome']
            aux['preco'] = pacote['Fidelizacao_24Meses']['preco']

            if pacote['canais'] is None and pacote['phone'] is None:
                aux['servico'] = 'NET'
            elif pacote['net'] is None and pacote['phone'] is None:
                aux['servico'] = 'TV'
            elif pacote['phone'] is None:
                aux['servico'] = 'TV+NET'
            elif pacote['net'] is None:
                aux['servico'] = 'TV+VOZ'
            else:
                aux['servico'] = 'TV+NET+VOZ'

            lista.append(aux)
            aux = {}

        return lista


def fiber_packages(packages):
    """ Retrieve all packages of type 'Fibra'
    :param: list of packages
    """
    lista = []

    for pacote in packages:
        if pacote['tipo'] == 'Pacotes Fibra':
            lista.append(pacote)

    return lista


def satelite_packages(packages):
    """ Retrieve all packages of type 'Satélite'
    :param: list of packages
    """
    lista = []

    for pacote in packages:
        if pacote['tipo'] == 'Pacotes Satélite':
            lista.append(pacote)

    return lista


def packages_by_service(servico, packages):
    """ Retrieve all packages with specified service
    :param: service
    :param: list of packages
    """
    lista = []

    for pacote in packages:
        if servico.lower() == pacote['servico'].lower():
            lista.append(pacote)

    return lista


def packages_by_price(inf, sup, packages):
    """ Retrieves all avaiable packages that are within a specified price threshold
    :param: lowest value of price
    :param: highest value of price
    :param: list of packages
    """
    lista = []

    inf = str_to_float(inf)
    sup = str_to_float(sup)

    for pacote in packages:
        preco = str_to_float(pacote['preco'])

        if inf <= preco <= sup:
            lista.append(pacote)

    return lista