import requests
import re
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def clean(string):
    string = re.sub(r'(\n|\r|\s)+', ' ', string)
    string = re.sub(r'\s+', ' ', string)
    string = re.sub(r'^\s+', '', string)
    string = re.sub(r'\s+$', '', string)
    return string

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

###########################################################################################################

def get_linhas_apoio():
    r = requests.get("https://www.nos.pt/particulares/contactos/Pages/linhas-de-apoio.aspx")
    if (r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        soup = soup.find_all('div', {'class':'container__box'})
    return soup


def get_list_linhas_apoio(soup):
    lista_json = []
    for elem in soup:
        elem = elem.find('div',{'class':'island__description'})
        numero = elem.div['id']

        elem = elem.find('div',{})
        categoria = clean(elem.h2.text)

        elem.h2.clear()
        descricao = clean(elem.text)

        elem_json = {
            'categoria' :categoria,
            'numero' : numero,
            'descriçao' : descricao
        }

        lista_json.append(elem_json)
    return lista_json

########################################################################################################

def get_top_phones():
    r = requests.get("https://www.nos.pt/particulares/loja/Pages/loja-online.aspx")
    if (r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        soup = soup.find_all('div', {'class':'equipments-item-info col-divided'})

    return soup

def get_list_top_phones(soup):
    lista_json = []
    for elem in soup:
        nome = elem.find('a',{'class':'equipments-item-title masterTextColor'})
        preco = elem.find('div',{'class':'price-tag'})
        
        link = nome['href']
        nome = nome.text
        preco = preco.text.replace('€', '')

        elem_json = {
            'nome' :nome,
            'preço' : preco,
            'link' : link
        }

        lista_json.append(elem_json)
    return lista_json

########################################################################################################

def get_phones():
    #r = requests.get("https://www.nos.pt/particulares/loja-equipamentos/pages/store.aspx#!?Filter=~(ProductType~'telemoveis~ProductPrice~'0*7c1900)")
    #if (r.status_code == 200):

    options = Options()
    options.add_argument('--headless')
    # Create your driver
    driver = webdriver.Firefox(options=options)

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

    driver.quit()

    return(soup)

def get_list_phones(soup):
    lista_json = []
    taglista = []
    link_telemovel = 'https://www.nos.pt'
    prestações = 'Disponível'
    pontos = 'Disponível'
    for elem in soup:
        nome = elem.find('div',{'class':'properties-name ng-binding'})
        nome = nome.text

        tag = elem.find_all('em')
        for em in tag:
            taglista.append(em.text)

        preco = elem.find('div',{'class':'item-price__now ng-binding'})
        preco = preco.text.replace(' ', '').replace('€', '')

        link = elem.find('a', {'ng-href':True})
        link_telemovel = link_telemovel + link['href']

        prestacao = elem.find('li', {'ng-show':'showHasInstallmentPayment(equipment.Colors)'})
        prestacao2 = prestacao['class']
        if prestacao2 == ['ng-binding', 'ng-hide'] :
            prestações = 'Não disponível'

        points = elem.find('li', {'ng-show':'showHasPointsPayment(equipment.PointsPrices)'})
        points2 = points['class']
        if points2 == ['ng-binding', 'ng-hide'] :
            pontos = 'Não disponível'

        elem_json = {
            'nome' :nome,
            'preço' : preco,
            'tags' : taglista,
            'link' : link_telemovel,
            'prestações' : prestações,
            'pontos' : pontos
        }

        lista_json.append(elem_json)
        taglista = []
        link_telemovel = 'https://www.nos.pt'
        prestações = 'Disponível'
        pontos = 'Disponível'

    return lista_json

##########################################################################################################################################################

def create_json_file(lista_json, filename, sk):
    fich = open(os.path.dirname(os.path.abspath(__file__)) + '/../json/' + filename,'w')
    prettyJSON = json.dumps(lista_json,sort_keys=sk,indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
    fich.close()

##########################################################################################################################################################

def update():
    soup = get_linhas_apoio()
    lista = get_list_linhas_apoio(soup)
    create_json_file(lista, "linhas_apoio.json", True)

    soup2 = get_top_phones()
    lista2 = get_list_top_phones(soup2)
    create_json_file(lista2, "top_phones.json", False)

    soup3 = get_phones()
    lista3 = get_list_phones(soup3)
    create_json_file(lista3, "phones.json", False)

    soup4 = get_Wtf()
    create_json_file(soup4, "tarifario_WTF.json", True)
