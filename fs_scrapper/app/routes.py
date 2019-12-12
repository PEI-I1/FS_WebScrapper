from app import app
from app import handler
from flask import jsonify, request


@app.route('/fs_scrapper/')
@app.route('/fs_scrapper/index')
def index():
    return "Hello, World!"


@app.route('/fs_scrapper/linhas_apoio')
def linhas_apoio_assunto_request():
    assunto = request.args.get('assunto')
    if not assunto:
        return jsonify(response = handler.linhas_apoio())
    else:
        return jsonify(response = handler.linhas_apoio_assunto(assunto))


@app.route('/fs_scrapper/phone_model/<model>')
def phone_model_request(model):
    return jsonify(response = handler.phone_model(model))


@app.route('/fs_scrapper/brand_phones/<brand>')
def brand_phones_request(brand):
    return jsonify(response = handler.brand_phones(brand))


@app.route('/fs_scrapper/top_phones')
def top_phones_request():
    return jsonify(response = handler.top_phones())


@app.route('/fs_scrapper/promo_phones')
def promo_phones_request():
    return jsonify(response = handler.promo_phones())


@app.route('/fs_scrapper/new_phones')
def new_phones_request():
    return jsonify(response = handler.new_phones())


@app.route('/fs_scrapper/ofer_phones')
def ofer_phones_request():
    return jsonify(response = handler.ofer_phones())


@app.route('/fs_scrapper/prest_phones')
def prest_phones_request():
    return jsonify(response = handler.prest_phones())


@app.route('/fs_scrapper/points_phones')
def points_phones_request():
    return jsonify(response = handler.points_phones())


@app.route('/fs_scrapper/phones_price/<float:min>/<float:max>')
def phones_price_request(min, max):
    return jsonify(response = handler.phones_by_price(min, max))


@app.route('/fs_scrapper/phones_brand_price/<string:brand>/<float:min>/<float:max>')
def phones_brand_price_request(brand, min, max):
    return jsonify(response = handler.phones_brand_price(brand, min, max))


@app.route('/fs_scrapper/phones_brand_promo/<string:brand>')
def phones_brand_promo_request(brand):
    return jsonify(response = handler.phones_brand_promo(brand))


@app.route('/fs_scrapper/phones_promo_price/<float:min>/<float:max>')
def phones_promo_price_request(min, max):
    return jsonify(response = handler.phones_promo_price(min, max))


@app.route('/fs_scrapper/new_phones_brand/<string:brand>')
def new_phones_brand_request(brand):
    return jsonify(response = handler.new_phones_brand(brand))


@app.route('/fs_scrapper/all_wtf')
def all_wtf_request():
    return jsonify(response = handler.all_wtf())


@app.route('/fs_scrapper/wtf_name/<string:name>')
def wtf_name_request(name):
    return jsonify(response = handler.wtf_name(name))


@app.route('/fs_scrapper/stores_zone/<string:zone>')
def stores_zone_request(zone):
    return jsonify(response = handler.stores_by_zone(zone))


@app.route('/fs_scrapper/store_address/<string:address>')
def store_address_request(address):
    return jsonify(response = handler.store_address(address))


@app.route('/fs_scrapper/stores_coordinates/<float:lat>/<float:lon>')
def stores_coordinates_request(lat, lon):
    return jsonify(response = handler.stores_by_coordinates(lat, lon))


@app.route('/fs_scrapper/specific_package/<string:tipo>/<string:nome>')
def specific_package_request(tipo, nome):
    return jsonify(response = handler.specific_package(tipo, nome))


@app.route('/fs_scrapper/packages')
def packages_request():
    return jsonify(response = handler.packages())


@app.route('/fs_scrapper/fiber_packages')
def fiber_packages_request():
    return jsonify(response = handler.fiber_packages())


@app.route('/fs_scrapper/satelite_packages')
def satelite_packages_request():
    return jsonify(response = handler.satelite_packages())


@app.route('/fs_scrapper/packages_service/<string:servico>')
def packages_service_request(servico):
    return jsonify(response = handler.packages_by_service(servico))


@app.route('/fs_scrapper/packages_price/<float:min>/<float:max>')
def packages_price_request(min, max):
    return jsonify(response = handler.packages_by_price(min, max))


@app.route('/fs_scrapper/packages_service_price/<string:service>/<float:min>/<float:max>')
def packages_service_price_request(service, min, max):
    return jsonify(response = handler.packages_service_price(service, min, max))


@app.route('/fs_scrapper/fiber_packages_price/<float:min>/<float:max>')
def fiber_packages_price_request(min, max):
    return jsonify(response = handler.fiber_packages_price(min, max))


@app.route('/fs_scrapper/satelite_packages_price/<float:min>/<float:max>')
def satelite_packages_price_request(min, max):
    return jsonify(response = handler.satelite_packages_price(min, max))


@app.route('/fs_scrapper/fiber_packages_service/<string:servico>')
def fiber_packages_service_request(servico):
    return jsonify(response = handler.fiber_packages_service(servico))


@app.route('/fs_scrapper/satelite_packages_service/<string:servico>')
def satelite_packages_service_request(servico):
    return jsonify(response = handler.satelite_packages_service(servico))
