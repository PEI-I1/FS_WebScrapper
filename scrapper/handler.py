#!/usr/bin/python3
import json
from re import sub


def linhasApoio(assunto):
    with open('linhas_apoio.json', 'r') as f:
        data = json.load(f)
        lista = []

        for linha in data:
            if linha['categoria'].lower() == assunto.lower():
                lista.append(linha)
                return lista

            elif assunto.lower() in linha['categoria'].lower():
                lista.append(linha)
        
        return lista


def phoneModel(modelo):
    with open('phones.json', 'r') as f:
        data = json.load(f)
        aux = {}

        for phone in data:
            if phone['nome'].lower() == modelo.lower():
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                aux['tags'] = phone['tags']
                aux['link'] = phone['link']
                aux['pretacoes'] = phone['prestações']
                aux['pontos'] = phone['pontos']
                return aux


def brandPhones(marca):
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if marca.lower() in phone['nome'].lower():
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def topPhones():
    with open('topPhones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            aux['nome'] = phone['nome']
            aux['preco'] = phone['preço']
            lista.append(aux)
            aux = {}

        return lista


def promoPhones():
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if 'desconto' in phone['tags']:
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def newPhones():
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if 'novidade' in phone['tags']:
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def oferPhones():
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            for tag in phone['tags']:
                if 'oferta' in tag:
                    aux['nome'] = phone['nome']
                    aux['preco'] = phone['preço']
                    aux['oferta'] = tag
                    lista.append(aux)
                    aux = {}

        return lista


def prestPhones():
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if phone['prestações'] == 'Disponível':
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def pontosPhones():
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            if phone['pontos'] == 'Disponível':
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def phonesByPrice(inf, sup):
    with open('phones.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for phone in data:
            aux1 = sub(r'[^\d,]', '', phone['preço'])
            aux2 = sub(r',', '.', aux1)
            preco = float(aux2)

            if inf <= preco <= sup:
                aux['nome'] = phone['nome']
                aux['preco'] = phone['preço']
                lista.append(aux)
                aux = {}

        return lista


def allWtf():
    with open('tarifario_WTF.json', 'r') as f:
        data = json.load(f)
        lista = []
        aux = {}

        for tarifario in data:
            aux['nome'] = tarifario['Nome_Tarifario']
            aux['preco'] = tarifario['Preco']
            lista.append(aux)
            aux = {}

        return lista


def wtfNome(nome):
     with open('tarifario_WTF.json', 'r') as f:
        data = json.load(f)
        aux = {}

        for tarifario in data:
            if tarifario['Nome_Tarifario'].lower() == nome.lower():
                aux['nome'] = tarifario['Nome_Tarifario']
                aux['preco'] = tarifario['Preco']
                aux['preco_total'] = tarifario['Preco_Total']
                aux['minutos'] = tarifario['Minutos']
                aux['net'] = tarifario['Net']
                aux['sms'] = tarifario['SMS']
                aux['cinema'] = tarifario['Cinema']
                aux['uber'] = tarifario['Uber']
                aux['uber_eats'] = tarifario['Uber_eats']
                return aux

