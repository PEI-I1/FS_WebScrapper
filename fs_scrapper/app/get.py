import requests
import re
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def clean(string):
    string = re.sub(r'\s+', ' ', string)
    string = re.sub(r'^\s+', '', string)
    string = re.sub(r'\s+$', '', string)
    return string

def exists(array, key, value):
    n = len(array)
    i = 0
    found = False

    while i < n and not found:
        if array[i][key] == value:
            found = True
        i += 1

    return found

#################################################### WTF ##################################################

def get_Wtf():
    r = requests.get("https://www.wtf.pt/")
    soup = None
    if(r.status_code == 200):
            soup = BeautifulSoup(r.text, 'html.parser')
            soup = soup.find_all('div', {'class':'section-tarifario__block__body'})
    
    lista_json = []
    for elem in soup:
        #nome Tarifario
        elema = elem.find('div',{'class':'section-tarifario__block__header d-flex justify-content-between'})
        nomeTarifario = elema.find('span',{'class':'section-tarifario__block__header-text-name-pack'}).text
        #custo
        elemb = elem.find('div',{'class':'section-tarifario__block__header-prices'})
        preco = elem.find('span', {'class':'section-tarifario__block__header-text-price'}).text.replace('€', '')
        periodo = elem.find('span', {'class':'section-tarifario__block__header-text-name-price-week'}).text
        total = elem.find('span', {'class':'section-tarifario__block__header-text-price-total'}).text.replace('€', '')
        
        #net
        elemNet = elem.find('div',{'class':'section-tarifario__block__tabs'})
        gigaA = elemNet.find('span',{'class':'block-tab__text-limit d-block'}).text
        giga = clean(gigaA)
        #minutos
        elemMin = elemNet.find('span',{'class':'block-tab__text-limit d-block text-yellow'}).text
        text1 = elemNet.find('span',{'class':'block-tab__text-sublimit text-yellow d-block'}).text
        text2 = elemNet.find('span',{'class':'block-tab__text-limit d-block'}).text
        text3 = elemNet.find('div',{'class':'w-100 mt-3'})
        text3Aux = text3.find('span',{'class':'block-tab__text-limit d-block'}).text
        text3Aux1 = text3.find('span',{'class':'block-tab__text-sublimit d-block'}).text
        #extras
        elemExtra = elem.find('div',{'class':'panel panel-default tab-pink'})
        elemExtratxt = elemExtra.find('span', {'class':'block-tab__text-limit d-block text-yellow'}).text
        elemExtratxt2 = elemExtra.find('span', {'class':'block-tab__text-sublimit d-block mt-2'}).text
        elemExtratxt3 = elem.find('div', {'class':'w-100 text-center mt-3'})
        elemAux = elemExtratxt3.find_all('span', {'class':'block-tab__text-sublimit d-block mt-2'})
        lista = []

        for em in elemAux: 
            lista.append(em.text)

        elem_json = {
            'Nome_Tarifario' :nomeTarifario,
            'Preco' : preco + periodo,
            'Preco_Total' : total,
            'Net' : giga,
            'Minutos' : elemMin + " " + text1,
            'SMS' : text3Aux + " " + text3Aux1,
            'Cinema' : elemExtratxt,
            'Uber' : elemExtratxt2,
            'Uber_eats' : lista[1]
        }

        lista_json.append(elem_json)

    del soup

    return lista_json


def get_linhas_apoio():
    r = requests.get("https://www.nos.pt/particulares/contactos/Pages/linhas-de-apoio.aspx")
    if (r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        soupA = soup.find_all('div', {'class':'container__box'})

    return soupA


def get_linhas_apoio_Price():
    r = requests.get("https://www.nos.pt/particulares/contactos/Pages/linhas-de-apoio.aspx")
    if (r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        soupA = soup.find_all('div', {'class':'panel__content one-whole'})

    return soupA


def remove_html_tags(text):
    """Remove html tags from a string"""
    text = re.sub('/\s\s+/g', ' ',text)
    text = re.sub('\\n|\\r', '', text)
    text = re.sub('Serviços disponibilizados:.*(?=\.).', '', text)
    text = re.sub('Custo da chamada', '', text)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_list_linhas_apoio(soup):
    lista_json = []
    it = 1
    precoInfo = get_linhas_apoio_Price()
    for elem in soup:
        otherInfo = elem.find_all('div',{'class':'island__description'})
        for a in otherInfo:
            if a.find('img',{'src' : '/particulares/contactos/PublishingImages/horario.png'}) is not None:
                horario = a.text
                horario = re.sub('\\n|\\r', '', horario)

        elem = elem.find('div',{'class':'island__description'})
        numero = elem.div['id']

        preco = precoInfo[it].text
        preco = remove_html_tags(preco)

        elem = elem.find('div',{})
        categoria = clean(elem.h2.text)

        elem.h2.clear()
        descricao = clean(elem.text)

        elem_json = {
            'categoria' :categoria,
            'numero' : numero,
            'descricao' : descricao,
            'horario' : horario,
            'preco': preco
        }
        it = it + 1
        lista_json.append(elem_json)
    return lista_json


def get_caracteristics(driver, phone):
    if phone['link']:
        driver.get(phone['link'])

        try:
            wait = WebDriverWait(driver, 5)
            location = (By.CLASS_NAME, "equipments-detail__tech-specs card container--fixed")
            element_present = EC.presence_of_element_located(location)
            wait.until(element_present)
        except:
            pass

        text = driver.page_source

        if text:
            image_links = re.findall(r'class="item item--equipment ng-scope[^"]*"[^/]*//([^)]*)\)', text)
            preco_original = re.findall(r'class="header-price__old  ng-binding"[^>]*>([^<]*)<', text)
            processador = re.findall(r'>processador</span>[^<]*<span[^>]*>([^<]*)<', text)
            memoria = re.findall(r'>memória</span>[^<]*<span[^>]*>([^<]*)<', text)
            camara = re.findall(r'>câmara</span>[^<]*<span[^>]*>(.*)</span>', text)

            if len(preco_original):
                preco_original = preco_original[0].replace('€','')
                phone['preco_original'] = clean(preco_original)

            if len(image_links):
                phone['image_link'] = "http://" + image_links[0]

            if len(processador):
                phone['processador'] = clean(processador[0])

            if len(memoria):
                phone['memoria'] = clean(memoria[0])

            if len(camara):
                camara = re.sub(r'\s*<br>\s*', '\\n         ', camara[0])
                camara = re.sub(r'<[^>]+>', '', camara)
                camara = re.sub(r'\s+$', '', camara)
                phone['camara'] = camara

def get_top_phones():
    r = requests.get("https://www.nos.pt/particulares/loja/Pages/loja-online.aspx")
    if (r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        soup = soup.find_all('div', {'class':'equipments-item-info col-divided'})

    return soup

def get_list_top_phones(driver, soup):
    lista_json = []

    for elem in soup:
        nome = elem.find('a',{'class':'equipments-item-title masterTextColor'})
        link = nome['href']

        if not exists(lista_json, "link", link):
            nome = nome.text

            preco = elem.find('div',{'class':'price-tag'})
            preco = preco.text.replace('€', '')

            elem_json = {
                'nome' :nome,
                'preco' : preco,
                'link' : link
            }

            get_caracteristics(driver, elem_json)
            lista_json.append(elem_json)

    return lista_json


def get_phones(driver):
    #r = requests.get("https://www.nos.pt/particulares/loja-equipamentos/pages/store.aspx#!?Filter=~(ProductType~'telemoveis~ProductPrice~'0*7c1900)")
    #if (r.status_code == 200):

    # Get a page
    driver.get("https://www.nos.pt/particulares/loja-equipamentos/pages/store.aspx#!?Filter=~(ProductType~'telemoveis~ProductPrice~'0*7c1900)")
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    # Feed the source to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find_all('div',{'class':'content-item__wrapper'})

    return(soup)

def get_list_phones(driver, soup):
    lista_json = []
    taglista = []
    link_telemovel = 'https://www.nos.pt'
    prestações = 'Disponível'
    pontos = 'Disponível'

    for elem in soup:
        link = elem.find('a', {'ng-href':True})
        link_telemovel = link_telemovel + link['href']

        if not exists(lista_json, "link", link_telemovel):
            nome = elem.find('div',{'class':'properties-name ng-binding'})
            nome = nome.text

            tag = elem.find_all('em')
            for em in tag:
                taglista.append(em.text)

            preco = elem.find('div',{'class':'item-price__now ng-binding'})
            preco = preco.text.replace(' ', '').replace('€', '')

            prestacao = elem.find('li', {'ng-show':'showHasInstallmentPayment(equipment.Colors)'})
            if prestacao is not None:
                prestacao2 = prestacao['class']
                if prestacao2 == ['ng-binding', 'ng-hide'] :
                    prestações = 'Não disponível'

            points = elem.find('li', {'ng-show':'showHasPointsPayment(equipment.PointsPrices)'})
            if points is not None:
                points2 = points['class']
                if points2 == ['ng-binding', 'ng-hide'] :
                    pontos = 'Não disponível'

            elem_json = {
                'nome' :nome,
                'preco' : preco,
                'tags' : taglista,
                'link' : link_telemovel,
                'prestacoes' : prestações,
                'pontos' : pontos
            }

            get_caracteristics(driver, elem_json)
            lista_json.append(elem_json)

            taglista = []
            prestações = 'Disponível'
            pontos = 'Disponível'

        link_telemovel = 'https://www.nos.pt'

    return lista_json


def create_json_file(lista_json, filename, sk):
    fich = open(os.path.dirname(os.path.abspath(__file__)) + '/../json/' + filename,'w')
    prettyJSON = json.dumps(lista_json,sort_keys=sk,indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
    fich.flush()
    os.fsync(fich)
    fich.close()


def update():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    print("[FS_SCRAPPER] Starting Update of top phones...")
    soup = get_top_phones()
    lista = get_list_top_phones(driver, soup)
    create_json_file(lista, "top_phones.json", False)
    print("[FS_SCRAPPER] Updated top phones!")

    print("[FS_SCRAPPER] Starting Update of phones...")
    soup = get_phones(driver)
    lista = get_list_phones(driver, soup)
    create_json_file(lista, "phones.json", False)
    print("[FS_SCRAPPER] Updated phones!")

    driver.quit()

    print("[FS_SCRAPPER] Starting Update of support lines...")
    soup = get_linhas_apoio()
    lista = get_list_linhas_apoio(soup)
    create_json_file(lista, "linhas_apoio.json", True)
    print("[FS_SCRAPPER] Updated support lines!")

    print("[FS_SCRAPPER] Starting Update of tariffs WTF...")
    soup = get_Wtf()
    create_json_file(soup, "tarifario_WTF.json", True)
    print("[FS_SCRAPPER] Updated tariffs WTF!")
