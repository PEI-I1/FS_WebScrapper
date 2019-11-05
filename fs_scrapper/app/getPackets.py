import requests
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LINK: https://www.nos.pt/particulares/pacotes/todos-os-pacotes/Paginas/precario.aspx#3 


###########################################################################################################
###########################################################################################################
def getPackets():
    link = 'https://www.nos.pt/particulares/pacotes/todos-os-pacotes/Paginas/precario.aspx#3'

    r = requests.get(link)
    if(r.status_code == 200):
            soup = BeautifulSoup(r.text, 'html.parser')
            soup = soup.find('div', {'class':'tabelaFid'})
    
    sections = []
    sections = soup.findAll('section')
    listaElementos = []
    
    for item in sections:
        tipo = getTipoPacote(item)
        
        lista = []
        lista = soup.find_all('article') # cada article é um pacote
        i = 0
        for elem in lista: 
            # Uso de try's porque os pacotes podem ou não incluir os diversos serviços
                #print(elem)
            nome = canais = net = phone = mobile = netmovel = None
            try: nome = elem.find('h3').text 
            except: pass
            try: canais = elem.find('p',{'class':'tv'}).text
            except: pass
            try: net = elem.find('p',{'class':'net'}).text
            except: pass
            try: phone = elem.find('p',{'class':'phone'}).text
            except: pass
            try: mobile = elem.find('p',{'class':'mobile'}).text
            except: pass
            try: netmovel = elem.find('p',{'class':'netmovel'}).text
            except: pass
               
            headers = elem.find_all('div', {}) 
            col1 = getFirstColumn(headers)
            col2 = getSecondColumn(headers)
            col3 = getThirdColumn(headers)
            col4 = getFourthColumn(headers)   

            thisDict = {
                'Tipo' : tipo,
                'nome' : nome,
                'canais' : canais, 
                'net' : net,
                'phone' : phone,
                'mobile' : mobile,
                'netMovel' : netmovel,
                'Fidelizacao_24Meses' : col1,
                'Fidelizacao_12Meses' : col2,
                'Fidelizacao_6Meses' : col3,
                'Sem_Fidelizacao' : col4
            }
            listaElementos.append(thisDict)   
        
    sendToJSON(listaElementos)
    

def getTipoPacote(soup):
    
    tipoFibra = tipoSatelite = None

    try:tipoFibra = soup.find('h2',{'class':'masterTextColorA'}).text
    except: pass
    try: tipoSatelite = soup.find('h2',{'class':'masterTextColorB'}).text
    except: pass

    if tipoFibra is not None:
        tipo = tipoFibra
    else:
        tipo = tipoSatelite
        
    return tipo

def getFirstColumn(soup):
    #print(soup[0])
    preco = soup[0].find('em').text
    listaVantagens =  []
    lista = soup[0].find('div',{'class':'mais'}).find_all('p')
    precoAdesao = soup[0].find('span').text

    for elem in lista:
        e = re.sub(r'(€[0-9,]*)',r'\1 euros',elem.text)
        listaVantagens.append(e.replace('€', ''))

    thisDict = {
        'Fidelizacao': "24 Meses",
        'preco':preco,
        'precoAdesao': precoAdesao,
        'Vantagens' : listaVantagens
    }

    return thisDict

    

def getSecondColumn(soup):
    #print(soup[2])
    preco = soup[2].find('em').text
    listaVantagens =  []
    lista = soup[2].find('div',{'class':'mais'}).find_all('p')
    precoAdesao = soup[2].find('span').text

    for elem in lista:
        e = re.sub(r'(€[0-9,]*)',r'\1 euros',elem.text)
        listaVantagens.append(e.replace('€', ''))

    thisDict = {
        'Fidelizacao': "12 Meses",
        'preco':preco,
        'precoAdesao': precoAdesao,
        'Vantagens' : listaVantagens
    }

    return thisDict


def getThirdColumn(soup):
    #print(soup[4])
    preco = soup[4].find('em').text
    listaVantagens =  []
    lista = soup[4].find('div',{'class':'mais'}).find_all('p')
    precoAdesao = soup[4].find('span').text

    for elem in lista:
        e = re.sub(r'(€[0-9,]*)',r'\1 euros',elem.text)
        listaVantagens.append(e.replace('€', ''))

    thisDict = {
        'Fidelizacao': "6 Meses",
        'preco':preco,
        'precoAdesao': precoAdesao,
        'Vantagens' : listaVantagens
    }
    
    return thisDict


def getFourthColumn(soup):
    #print(soup[6])
    preco = soup[6].find('em').text
    listaVantagens =  []
    lista = soup[6].find('div',{'class':'mais'}).find_all('p')
    precoAdesao = soup[6].find('span').text

    for elem in lista:
        e = re.sub(r'(€[0-9,]*)',r'\1 euros',elem.text)
        listaVantagens.append(e.replace('€', ''))

    thisDict = {
        'Fidelizacao': "Sem Fidelizacao",
        'preco':preco,
        'precoAdesao': precoAdesao,
        'Vantagens' : listaVantagens
    }  
    
    return thisDict

def sendToJSON(dic):
    fich = open('Pacotes.json','w')
    prettyJSON = json.dumps(dic, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
    fich.close()
###########################################################################################################
###########################################################################################################

getPackets()