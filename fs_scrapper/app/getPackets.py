import requests
import re
import json
import os
from app import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LINK: https://www.nos.pt/particulares/pacotes/todos-os-pacotes/Paginas/precario.aspx#3 

def getText(tag):
    ret = ""
    if '<span' in str(tag):
        ret = tag.text
    else:
        ret = str(tag)

    ret = get.clean(ret)
    return ret

def getPretty(elem, tag, cl):
    aux = map(getText, elem.find(tag, {'class': cl}).contents)
    aux = filter(None, aux)

    return ", ".join(aux)

###########################################################################################################
###########################################################################################################
def getPackets():
    link = 'https://www.nos.pt/particulares/pacotes/todos-os-pacotes/Paginas/precario.aspx'

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
            try: nome = get.clean(elem.find('h3').text)
            except: pass
            try: canais = getPretty(elem, 'p', 'tv')
            except: pass
            try: net = getPretty(elem, 'p', 'net')
            except: pass
            try: phone = getPretty(elem, 'p', 'phone')
            except: pass
            try: mobile = getPretty(elem, 'p', 'mobile') 
            except: pass
            try: netmovel = getPretty(elem, 'p', 'netmovel')
            except: pass

               
            headers = elem.find_all('div', {}) 
            col1 = getColumn(headers, 1, "24 Meses")
            col2 = getColumn(headers, 2, "12 Meses")
            col3 = getColumn(headers, 3, "6 Meses")
            col4 = getColumn(headers, 4, "Sem Fidelizacao")

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

    #getLinks(listaElementos)
        
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


def getColumn(soup, col, fid):
    col_idx = (col<<1) - 2
    preco = soup[col_idx].find('em').text
    listaVantagens =  []
    lista = soup[col_idx].find('div',{'class':'mais'}).find_all('p')
    precoAdesao = soup[col_idx].find('span').text

    for elem in lista:
        e = re.sub(r'(€[0-9,]*)',r'\1 euros',elem.text)
        listaVantagens.append(e.replace('€', ''))

    thisDict = {
        'Fidelizacao': fid,
        'preco':preco,
        'precoAdesao': precoAdesao,
        'Vantagens' : listaVantagens
    }

    return thisDict


#def getLinks(lista):
#    link = "https://www.nos.pt/particulares/pacotes/todos-os-pacotes/Paginas/pacotes.aspx"
#    links = []
#
#    r = requests.get(link)
#    if(r.status_code == 200):
#        options = Options()
#        options.add_argument('--headless')
#        driver = webdriver.Firefox(options=options)
#
#        linksS = []
#        sections = r.text.split('<section class="box')
#        for sec in sections:
#            tipo = re.search(r'^[^"]*', sec)
#            tipo = tipo.group(0)
#            tipo = re.sub('Satelite','Satélite', tipo)
#
#            aux = re.findall(r'(?:<h2>([^<]*)</h2>[^"]*)?"([^"]*detalhe(?:-pacote)?.aspx[^"]*)"', sec)
#            for (n,l) in aux:
#                ls = {'tipo': tipo, 'nome': n, 'link': l}
#                if ls not in linksS:
#                    linksS.append(ls)
#
#        for l in linksS:
#            time.sleep(3)
#            driver.get(l['link'])
#            soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#            try:
#                preco = soup.find('div', {'class': 'price__value ng-binding'})
#                preco = str(preco.contents[0])
#            except:
#                preco = soup.find('span', {'class': 'total'})
#                print(preco)
#                try:
#                    preco = str(preco.text)
#                except:
#                    print(l['link'])
#                    preco = ""
#
#            preco = re.sub(r'(\s|€|/)+','', preco)
#
#            if l['tipo'] and l['nome'] and preco:
#                ls = {'tipo': 'Pacotes ' + l['tipo'], 'nome': l['nome'], 'preco': preco, 'link': l['link']}
#                if ls not in links:
#                    links.append(ls)
#
#        driver.quit()
#
#    n = len(links)
#    f = 0
#    for e in lista:
#        found = False
#        i = 0
#        while i < n and not found:
#            if e['Tipo'] == links[i]['tipo'] and \
#              e['nome'] == links[i]['nome'] and \
#              e['Fidelizacao_24Meses']['preco'] == links[i]['preco']:
#                f += 1
#                found = True
#                e['link'] = links[i]['link']
#                print(links[i])
#            i += 1
#    print(n)
#    print(f)

def sendToJSON(dic):
    fich = open(os.path.dirname(os.path.abspath(__file__)) + '/../json/Pacotes.json','w')
    prettyJSON = json.dumps(dic, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
    fich.close()
###########################################################################################################
###########################################################################################################

def update():
    getPackets()
