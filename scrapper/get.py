import requests
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#################################################### WTF ##################################################
###########################################################################################################
def get_Wtf():
    r = requests.get("https://www.wtf.pt/")
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
        preco = elem.find('span', {'class':'section-tarifario__block__header-text-price'}).text
        periodo = elem.find('span', {'class':'section-tarifario__block__header-text-name-price-week'}).text
        total = elem.find('span', {'class':'section-tarifario__block__header-text-price-total'}).text
        
        #net
        elemNet = elem.find('div',{'class':'section-tarifario__block__tabs'})
        gigaA = elemNet.find('span',{'class':'block-tab__text-limit d-block'}).text
        giga = re.sub(r'[\\n|\\r|\s]','',gigaA)
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
    return lista_json

def create_json_file_TarifarioWTF(lista_json):
    fich = open('tarifario_WTF.json','w')
    prettyJSON = json.dumps(lista_json,sort_keys=True, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
###########################################################################################################
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
        categoria = elem.h2.text

        elem.h2.clear()
        descricao = elem.text

        elem_json = {
            'categoria' :categoria,
            'numero' : numero,
            'descriçao' : descricao
        }

        lista_json.append(elem_json)
    return lista_json


def create_json_file_linhas_apoio(lista_json):
    fich = open('linhas_apoio.json','w')
    prettyJSON = json.dumps(lista_json,sort_keys=True, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)

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
        preco = preco.text

        elem_json = {
            'nome' :nome,
            'preço' : preco,
            'link' : link
        }

        lista_json.append(elem_json)
    return lista_json


def create_json_file_top_phones(lista_json):
    fich = open('top_phones.json','w')
    prettyJSON = json.dumps(lista_json, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)

########################################################################################################

def get_phones():
    #r = requests.get("https://www.nos.pt/particulares/loja-equipamentos/pages/store.aspx#!?Filter=~(ProductType~'telemoveis~ProductPrice~'0*7c1900)")
    #if (r.status_code == 200):

    # Create your driver
    driver = webdriver.Firefox()

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
        preco = preco.text

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


def create_json_file_phones(lista_json):
    fich = open('phones.json','w')
    prettyJSON = json.dumps(lista_json, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)


#################################################################### Lojas e Informações #################################################################
##########################################################################################################################################################

def getLista_Lojas():
    print("A ir buscar a lista de Lojas")
    options = Options()
    options.add_argument('--headless')
    # Create your driver
    driver = webdriver.Firefox(options=options)

    # Get a page
    webPage = "https://www.nos.pt/particulares/Pages/lojas-nos.aspx"
    driver.get(webPage)
    
    # Feed the source to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lojas = soup.find_all('li',{'class':'resltLojas__single ng-scope'})
    listaLojas = []

    for loja in lojas:
        nomeLoja = loja.find('h3', {'class':'title ng-binding'}).text
        listaLojas.append(nomeLoja)

    print("Lista de Lojas obtida")
    driver.quit()
    
    return listaLojas
    
def getInfoLoja(nome):

    options = Options()
    options.add_argument('--headless')
    # Create your driver
    driver = webdriver.Firefox(options=options)
    listaServicos = []
    # Get a page
    webPage = "https://www.nos.pt/particulares/Pages/lojas-nos.aspx"
    driver.get(webPage)
    
    # Feed the source to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lojas = soup.find_all('li',{'class':'resltLojas__single ng-scope'})
          
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, nome)))
    try: element.click()
    except: pass

    if(element is not None):

        soupA = BeautifulSoup(driver.page_source, 'html.parser')
        soupA = soupA.find_all('div',{'class':'one-half h-100 pvendas_content pvendas_content--detail full-container container-xs-sm h-100'})
    
        nomeLoja = soupA[0].find('h2',{'class':'page-title hidden-xs-sm ng-binding'}).text
        morada = soupA[0].find('p',{'class':'pvenda-infoModule__txt ng-binding'}).text
            #print(morada)
        horario = soupA[0].find('p',{'ng-bind-html':'selectedStore.Schedule | unsafe'}).text
            #print(horario)
        listaA = soupA[0].find('ul',{'class':'pvenda-infoModule__list'})
        listaAux = listaA.find_all('li')
        for elem in listaAux:
            listaServicos.append(elem.text)

        thisdict = {
            'nome' : nomeLoja,
            'morada' : morada,
            'horario' : horario,
            'ListaServs' : listaServicos
        }

    driver.quit()
    sendToJSON(thisdict)
    return thisdict
##########################################################################################################################################################
##########################################################################################################################################################

def sendToJSON(dic):
    fich = open('lojas.json','a')
    prettyJSON = json.dumps(dic, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
    fich.close()

def getLojasMain():
    listaLojas = getLista_Lojas()

    for elem in listaLojas:
        print("A ir buscar: " + elem)
        try: dic = getInfoLoja(elem)
        except: pass

##########################################################################################################################################################
##########################################################################################################################################################

soup = get_phones()
lista = get_list_phones(soup)
create_json_file_phones(lista)
#create_json_file_TarifarioWTF(get_Wtf())
#getLojasMain()