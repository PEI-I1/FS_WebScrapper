from app import app
from app import handler
from flask import jsonify, request


@app.route('/fs_scrapper/linhas_apoio')
def linhas_apoio_assunto_request():
    assunto = request.args.get('assunto')
    if not assunto:
        return jsonify(response = handler.linhas_apoio())
    else:
        return jsonify(response = handler.linhas_apoio_assunto(assunto))


@app.route('/fs_scrapper/phones')
def phones_request():
    brand = request.args.get('brand')
    new = request.args.get('new')
    promo = request.args.get('promo')
    top = request.args.get('top')
    ofer = request.args.get('ofer')
    prest = request.args.get('prest')
    points = request.args.get('points')
    min_value = request.args.get('min')
    max_value = request.args.get('max')

    lista = handler.all_phones()

    if brand:
        lista = handler.brand_phones(brand, lista)
    if new:
        lista = handler.new_phones(lista)
    if promo:
        lista = handler.promo_phones(lista)
    if top:
        lista = handler.top_phones(lista)
    if ofer:
        lista = handler.ofer_phones(lista)
    if prest:
        lista = handler.prest_phones(lista)
    if points:
        lista = handler.points_phones(lista)
    if max_value and min_value:
        lista = handler.phones_by_price(min_value, max_value, lista)

    if brand is None:
        lista_final = []
        if ofer is None:
            for phone in lista:
                aux = {}
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preco']
                aux['link'] = phone['link']
                lista_final.append(aux)
        else:
            for phone in lista:
                aux = {}
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preco']
                for tag in phone['tags']:
                    if 'oferta' in tag:
                        aux['oferta'] = tag
                aux['link'] = phone['link']
                lista_final.append(aux)
        lista = lista_final

    return jsonify(response = lista)


@app.route('/fs_scrapper/wtf')
def wtf_request():
    nome = request.args.get('nome')

    if nome:
        return jsonify(response = handler.wtf_name(nome))
    else:
        return jsonify(response = handler.all_wtf())


@app.route('/fs_scrapper/stores')
def stores_request():
    zone = request.args.get('search_term')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if lat and lon:
        return jsonify(response = handler.stores_by_coordinates(lat,lon))
    elif zone:
        return jsonify(response = handler.stores_by_zone(zone))
    else:
        return jsonify(response = [])


@app.route('/fs_scrapper/packages')
def packages_request():
    tipo = request.args.get('type')
    servico = request.args.get('service')
    min_value = request.args.get('min')
    max_value = request.args.get('max')
    nome = request.args.get('name')

    if servico:
        if nome:
            return jsonify(response = handler.specific_package(tipo, nome))
        elif max_value and min_value:
            if tipo:
                if tipo == 'satelite':
                    return jsonify(response = handler.satelite_packages_service_price(servico, min_value, max_value))
                else:
                    return jsonify(response = handler.fiber_packages_service_price(servico, min_value, max_value))
            else:
                return jsonify(response = handler.packages_service_price(servico, min_value, max_value))
        elif tipo:
            if tipo == 'satelite':
                return jsonify(response = handler.satelite_packages_service(servico))
            else:
                return jsonify(response = handler.fiber_packages_service(servico))
        else:
            return jsonify(response = handler.packages_by_service(servico))

    elif max_value and min_value:
        if tipo:
            if tipo == 'satelite':
                return jsonify(response = handler.satelite_packages_price(min_value, max_value))
            else:
                return jsonify(response = handler.fiber_packages_price(min_value, max_value))
        else:
            return jsonify(response = handler.packages_by_price(min_value, max_value))

    elif tipo:
        if tipo == 'satelite':
            return jsonify(response = handler.satelite_packages())
        else:
            return jsonify(response = handler.fiber_packages())

    elif nome:
        lista = handler.specific_package("satélite", nome)
        lista = lista + handler.specific_package("fibra", nome)
        return jsonify(response = lista)
    else:
        return jsonify(response = handler.packages())
