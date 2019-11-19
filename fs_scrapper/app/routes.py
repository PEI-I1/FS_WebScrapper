from app import app
from app import handler
from flask import jsonify


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/linhas_apoio')
def linhas_apoio_request():
    return jsonify(response = handler.linhas_apoio())


@app.route('/linhas_apoio/<assunto>')
def linhas_apoio_assunto_request(assunto):
    return jsonify(response = handler.linhas_apoio_assunto(assunto))


@app.route('/phone_model/<model>')
def phone_model_request(model):
    return jsonify(response = handler.phone_model(model))


@app.route('/brand_phones/<brand>')
def brand_phones_request(brand):
    return jsonify(response = handler.brand_phones(brand))


@app.route('/top_phones')
def top_phones_request():
    return jsonify(response = handler.top_phones())


@app.route('/promo_phones')
def promo_phones_request():
    return jsonify(response = handler.promo_phones())


@app.route('/new_phones')
def new_phones_request():
    return jsonify(response = handler.new_phones())


@app.route('/ofer_phones')
def ofer_phones_request():
    return jsonify(response = handler.ofer_phones())


@app.route('/prest_phones')
def prest_phones_request():
    return jsonify(response = handler.prest_phones())


@app.route('/points_phones')
def points_phones_request():
    return jsonify(response = handler.points_phones())


@app.route('/phones_price/<float:min>/<float:max>')
def phones_price_request(min, max):
    return jsonify(response = handler.phones_by_price(min, max))


@app.route('/phones_brand_price/<brand>/<float:min>/<float:max>')
def phones_brand_price_request(brand, min, max):
    return jsonify(response = handler.phones_brand_price(brand, min, max))


@app.route('/phones_brand_promo/<brand>')
def phones_brand_promo_request(brand):
    return jsonify(response = handler.phones_brand_promo(brand))


@app.route('/phones_promo_price/<float:min>/<float:max>')
def phones_promo_price_request(min, max):
    return jsonify(response = handler.phones_promo_price(min, max))


@app.route('/new_phones_brand/<brand>')
def new_phones_brand_request(brand):
    return jsonify(response = handler.new_phones_brand(brand))


@app.route('/all_wtf')
def all_wtf_request():
    return jsonify(response = handler.all_wtf())


@app.route('/wtf_name/<name>')
def wtf_name_request(name):
    return jsonify(response = handler.wtf_name(name))


@app.route('/stores_zone/<zone>')
def stores_zone_request(zone):
    return jsonify(response = handler.stores_by_zone(zone))


@app.route('/store_address/<address>')
def store_address_request(address):
    return jsonify(response = handler.store_address(address))


@app.route('/specific_package/<tipo>/<nome>')
def specific_package_request(tipo, nome):
    return jsonify(response = handler.specific_package(tipo, nome))


@app.route('/packages')
def packages_request():
    return jsonify(response = handler.packages())


@app.route('/fiber_packages')
def fiber_packages_request():
    return jsonify(response = handler.fiber_packages())


@app.route('/satelite_packages')
def satelite_packages_request():
    return jsonify(response = handler.satelite_packages())


@app.route('/packages_service/<servico>')
def packages_service_request(servico):
    return jsonify(response = handler.packages_by_service(servico))


@app.route('/packages_price/<float:min>/<float:max>')
def packages_price_request(min, max):
    return jsonify(response = handler.packages_by_price(min, max))


@app.route('/packages_service_price/<service>/<float:min>/<float:max>')
def packages_service_price_request(service, min, max):
    return jsonify(response = handler.packages_service_price(service, min, max))


@app.route('/fiber_packages_price/<float:min>/<float:max>')
def fiber_packages_price_request(min, max):
    return jsonify(response = handler.fiber_packages_price(min, max))


@app.route('/satelite_packages_price/<float:min>/<float:max>')
def satelite_packages_price_request(min, max):
    return jsonify(response = handler.satelite_packages_price(min, max))


@app.route('/fiber_packages_service/<servico>')
def fiber_packages_service_request(servico):
    return jsonify(response = handler.fiber_packages_service(servico))


@app.route('/satelite_packages_service/<servico>')
def satelite_packages_service_request(servico):
    return jsonify(response = handler.satelite_packages_service(servico))