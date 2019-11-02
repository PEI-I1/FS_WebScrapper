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
    lista = []
    lista = soup.find_all('article') # cada article é um pacote
    i = 0
    for elem in lista: 
        # Uso de try's porque os pacotes podem ou não incluir os diversos serviços
        if i < 1: # apenas vai buscar um elemento para testar
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
            headers = elem.find_all('div') # total de 4*2 elementos, 
          #  a = 0
            while headers: #TODO
                print(headers)
          #      headers[a] = 
          #      headers[a+1] =
          #      a = a + 2
        i = i+1
    

        


def getPacketsFiber(soup):
    print(soup)
    
def getPacketsSatelitte(soup):
    print(soup)
###########################################################################################################
###########################################################################################################
getPackets()