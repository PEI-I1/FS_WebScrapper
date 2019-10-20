import requests
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time


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

    return(soup)

def get_list_phones(soup):
    lista_json = []
    taglista = []
    link_telemovel = 'https://www.nos.pt'
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
        
        elem_json = {
            'nome' :nome,
            'preço' : preco,
            'tags' : taglista,
            'link' : link_telemovel
        }

        lista_json.append(elem_json)
        taglista = []
        link_telemovel = 'https://www.nos.pt'

    return lista_json


def create_json_file_phones(lista_json):
    fich = open('phones.json','w')
    prettyJSON = json.dumps(lista_json, indent=2,ensure_ascii=False)
    fich.write(prettyJSON)


soup = get_phones()
lista = get_list_phones(soup)
create_json_file_phones(lista)