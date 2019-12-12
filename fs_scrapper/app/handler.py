import json
from re import sub
from haversine import haversine, Unit


def linhas_apoio():
    """ Retrieve service lines
    """
    with open('json/linhas_apoio.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for linha in data:
            aux['categoria'] = linha['categoria']
            aux['numero'] = linha['numero']
            lista.append(aux)
            aux = {}

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


def phone_model(modelo):
    """ Retrieve the specified model
    :param: phone's model
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        aux = {}

        for phone in data:
            if phone['nome'].lower() == modelo.lower():
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                aux['tags'] = phone['tags']
                aux['link'] = phone['link']
                aux['pretacoes'] = phone['prestações']
                aux['pontos'] = phone['pontos']
                return aux


def brand_phones(marca):
    """ Retrieve all phones of specified brand
    :param: brand
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if marca.lower() in phone['nome'].lower():
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def brand_phones_aux(marca, data):
    lista = []

    for phone in data:
        if marca.lower() in phone['nome'].lower():
            lista.append(phone)

    return lista


def top_phones():
    """ Retrive the top most shearched/viewed phones
    """
    with open('json/top_phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            aux['nome'] = phone['nome']
            aux['preco'] = phone['preço']
            lista.append(aux)
            aux = {}

        return lista


def promo_phones():
    """ Retrieve all phones who are currently under a discount/promotion
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if 'desconto' in phone['tags']:
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def new_phones():
    """ Retrieve the most recents phones
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if 'novidade' in phone['tags']:
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def ofer_phones():
    """ Retrieve all the phones in which it comes with an offer
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            for tag in phone['tags']:
                if 'oferta' in tag:
                    aux['nome'] = phone['nome']
                    aux['preco'] = phone['preço']
                    aux['oferta'] = tag
                    lista.append(aux)
                    aux = {}

        return lista


def prest_phones():
    """ Retrieve all phones which have installment payment avaiable
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if phone['prestações'] == 'Disponível':
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def points_phones():
    """ Retrieve all phones which have points payment avaiable
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if phone['pontos'] == 'Disponível':
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def phones_by_price(inf, sup):
    """ Retrieve all phones which are in specified threshold of price
    :param: lowest number of price
    :param: highest number of price
    """
    with open('json/phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            aux1 = sub(r'[^\d,]', '', phone['preço'])
            aux2 = sub(r',', '.', aux1)
            preco = float(aux2)

            if inf <= preco <= sup:
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def phones_by_price_aux(inf, sup, data):
    lista = []

    for phone in data:
        aux1 = sub(r'[^\d,]', '', phone['preco'])
        aux2 = sub(r',', '.', aux1)
        preco = float(aux2)

        if inf <= preco <= sup:
            lista.append(phone)

    return lista


def phones_brand_price(marca, inf, sup):
    """ Retrieve all phones of specified brand which are in specified threshold of price
    :param: brand
    :param: lowest value of price
    :param: highest value of price
    """
    return phones_by_price_aux(inf, sup, brand_phones(marca))


def phones_brand_promo(marca):
    """ Retrieve all phones of specified brand which are currentelly under a discount/promotion
    :param: brand
    """
    return brand_phones_aux(marca, promo_phones())


def phones_promo_price(inf, sup):
    """ Retrieve all phones between a specified threshold of price which are currently under a discount/promotion
    :param: lowest value of price
    :param: highest value of price
    """
    return phones_by_price_aux(inf, sup, promo_phones())


def new_phones_brand(marca):
    """ Retrieve the most recents phones of specified brand
    :param: brand
    """
    return brand_phones_aux(marca, new_phones())


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
            lista.append(aux)
            aux = {}

        return lista


def wtf_name(nome):
    """ Retrieve information of specified tariff
    :param: tariff name
    """
    with open('json/tarifario_WTF.json', 'r') as f:
        data = json.load(f)
        aux = {}

        for tarifario in data:
            if tarifario['Nome_Tarifario'].lower() == nome.lower():
                aux['nome'] = tarifario['Nome_Tarifario']
                aux['preco'] = tarifario['Preco']
                aux['preco_total'] = tarifario['Preco_Total']
                aux['minutos'] = tarifario['Minutos']
                aux['net'] = tarifario['Net']
                aux['sms'] = tarifario['SMS']
                aux['cinema'] = tarifario['Cinema']
                aux['uber'] = tarifario['Uber']
                aux['uber_eats'] = tarifario['Uber_eats']
                return aux


def stores_by_zone(zona):
    """ Retrieve the stores avaiable at specified region
    :param: region
    """
    with open('json/lojas.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for loja in data:
            if zona.lower() == loja['localidade'] or zona.lower() in loja['morada'].lower():
                aux['nome'] = loja['nome']
                aux['morada'] = loja['morada']
                aux['horario'] = loja['horario']
                lista.append(aux)
                aux = {}

        return lista


def store_address(morada):
    """ Retrive information õf specified store with its address
    :param: store address
    """
    with open('json/lojas.json', 'r') as f:
        data = json.load(f)
        aux = {}

        for loja in data:
            if loja['morada'].lower() == morada.lower():
                aux['nome'] = loja['nome']
                aux['morada'] = loja['morada']
                aux['horario'] = loja['horario']
                aux['servicos'] = []

                for serv in loja['listaservs']:
                        aux['servicos'].append(serv)

                return aux


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


def specific_package(tipo, nome):
    """ Retrieve package of certain type and specific name
    :param: type of package
    :param: package name
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)

        for pacote in data:
            if pacote['Tipo'].lower() == tipo.lower() and pacote['nome'].lower() == nome.lower():
                return pacote


def packages():
    """ Retrieve all packages avaiable
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for pacote in data:
            aux['Tipo'] = pacote['Tipo']
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


def fiber_packages():
    """ Retrieve all packages of type 'Fibra'
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for pacote in data:
            if pacote['Tipo'] == 'Pacotes Fibra':
                aux['Tipo'] = pacote['Tipo']
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


def satelite_packages():
    """ Retrieve all packages of type 'Satélite'
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for pacote in data:
            if pacote['Tipo'] == 'Pacotes Satélite':
                aux['Tipo'] = pacote['Tipo']
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


def packages_by_service(servico):
    """ Retrieve all packages with specified service
    :param: service
    """
    lista = packages_by_service_aux(servico, packages())
    return lista


def packages_by_service_aux(servico, pacotes):
    lista = []

    for pacote in pacotes:
        if pacote['servico'] == servico:
            lista.append(pacote)

    return lista


def packages_by_price(inf, sup):
    """ Retrieves all avaiable packages that are within a specified price threshold
    :param: lowest value of price
    :param: highest value of price
    """
    with open('json/Pacotes.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for pacote in data:
            aux1 = sub(r',', '.', pacote['Fidelizacao_24Meses']['preco'])
            preco = float(aux1)

            if inf <= preco <= sup:
                aux['Tipo'] = pacote['Tipo']
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


def packages_by_price_aux(inf, sup, data):
    lista = []

    for pacote in data:
        aux = sub(r',', '.', pacote['preco'])
        preco = float(aux)

        if inf <= preco <= sup:
            lista.append(pacote)

    return lista


def packages_service_price(servico, inf, sup):
    """ Retrieves packages of a specific service that are within a specified price threshold
    :param: service
    :param: lowest value of price
    :param: highest value of price
    """
    return packages_by_service_aux(servico, packages_by_price(inf, sup))


def fiber_packages_price(inf, sup):
    """ Retrieves packages of type 'Fibra' that are within a specified price threshold
    :param: lowest value of price
    :param: highest value of price
    """
    return packages_by_price_aux(inf, sup, fiber_packages())


def satelite_packages_price(inf, sup):
    """ Retrieves packages of type 'Satélite' that are within a specified price threshold
    :param: lowest value of price
    :param: highest value of price
    """
    return packages_by_price_aux(inf, sup, satelite_packages())


def fiber_packages_service(servico):
    """ Retrieves packages of type 'Fibra' that have the specified service
    :param: service
    """
    return packages_by_service_aux(servico, fiber_packages())


def satelite_packages_service(servico):
    """ Retrieves packages of type 'Fibra' that have the specified service
    :param: service
    """
    return packages_by_service_aux(servico, satelite_packages())


# add método para net mínima
