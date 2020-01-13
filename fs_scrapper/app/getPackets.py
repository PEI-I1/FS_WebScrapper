import requests
import re
import json
import os
from app import get
from bs4 import BeautifulSoup

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


def sendToJSON(dic):
    fich = open(os.path.dirname(os.path.abspath(__file__)) + '/../json/Pacotes.json','w')
    prettyJSON = json.dumps(dic, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)
    fich.flush()
    os.fsync(fich)
    fich.close()


def update():
    getPackets()
