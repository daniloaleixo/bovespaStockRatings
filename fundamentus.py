#!/usr/bin/env python3

import re
import urllib.request
import urllib.parse
import http.cookiejar
import time

from lxml.html import fragment_fromstring
from collections import OrderedDict
from firebase import firebase
import json
import ast
import datetime
import os
from pymongo import MongoClient


def get_data(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min':'',
            'pl_max':'',
            'pvp_min':'',
            'pvp_max' :'',
            'psr_min':'',
            'psr_max':'',
            'divy_min':'',
            'divy_max':'',
            'pativos_min':'',
            'pativos_max':'',
            'pcapgiro_min':'',
            'pcapgiro_max':'',
            'pebit_min':'',
            'pebit_max':'',
            'fgrah_min':'',
            'fgrah_max':'',
            'firma_ebit_min':'',
            'firma_ebit_max':'',
            'margemebit_min':'',
            'margemebit_max':'',
            'margemliq_min':'',
            'margemliq_max':'',
            'liqcorr_min':'',
            'liqcorr_max':'',
            'roic_min':'',
            'roic_max':'',
            'roe_min':'',
            'roe_max':'',
            'liq_min':'',
            'liq_max':'',
            'patrim_min':'',
            'patrim_max':'',
            'divbruta_min':'',
            'divbruta_max':'',
            'tx_cresc_rec_min':'',
            'tx_cresc_rec_max':'',
            'setor':'',
            'negociada':'ON',
            'ordem':'1',
            'x':'28',
            'y':'16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    page = fragment_fromstring(reg)
    lista = OrderedDict()

    stocks = page.xpath('tbody')[0].findall("tr")

    for i in range(0, len(stocks)):
        lista[i] = {
            stocks[i].getchildren()[0][0].getchildren()[0].text: {
                'cotacao': stocks[i].getchildren()[1].text,
               'P/L': stocks[i].getchildren()[2].text,
               'P/VP': stocks[i].getchildren()[3].text,
               'PSR': stocks[i].getchildren()[4].text,
               'DY': stocks[i].getchildren()[5].text,
               'P/Ativo': stocks[i].getchildren()[6].text,
               'P/Cap.Giro': stocks[i].getchildren()[7].text,
               'P/EBIT': stocks[i].getchildren()[8].text,
               'P/Ativ.Circ.Liq.': stocks[i].getchildren()[9].text,
               'EV/EBIT': stocks[i].getchildren()[10].text,
               'EBITDA': stocks[i].getchildren()[11].text,
               'Mrg.Liq.': stocks[i].getchildren()[12].text,
               'Liq.Corr.': stocks[i].getchildren()[13].text,
               'ROIC': stocks[i].getchildren()[14].text,
               'ROE': stocks[i].getchildren()[15].text,
               'Liq.2m.': stocks[i].getchildren()[16].text,
               'Pat.Liq': stocks[i].getchildren()[17].text,
               'Div.Brut/Pat.': stocks[i].getchildren()[18].text,
               'Cresc.5a': stocks[i].getchildren()[19].text
               }
            }


    return lista


def get_specific_data(stock):
    url = "http://www.fundamentus.com.br/detalhes.php?papel=" + stock
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
    
    # Get data from site
    link = opener.open(url, urllib.parse.urlencode({}).encode('UTF-8'))
    content = link.read().decode('ISO-8859-1')

    # Get all table instances
    pattern = re.compile('<table class="w728">.*</table>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    reg = "<div>" + reg + "</div>"
    page = fragment_fromstring(reg)
    all_data = {}

    # There is 5 tables with tr, I will get all trs
    all_trs = []
    all_tables = page.xpath("table")

    for i in range(0, all_tables):
        all_trs = all_trs + all_tables[i].findall("tr")

    # Run through all the trs and get the label and the
    # data for each line
    for tr in all_trs:
        tr = all_trs[i]
        # Get into td
        all_tds = tr.getchildren()
        for i in range(0, all_tds):
            td = all_tds[i]

            label = ""
            data = ""

            # The page has tds with contents and some 
            # other with not
            if (td.get("class").find("label") != -1):
                # We have a label
                for span in td.getchildren():
                    if (span.get("class").find("txt") != -1):
                        label = span.text

                # If we did find a label we have to look 
                # for a value 
                if (len(label)) > 0:
                    next_td = all_tds[i + 1]

                    if (next_td.get("class").find("data") != -1):
                        # We have a data
                        for span in next_td.getchildren():
                            if (span.get("class").find("txt") != -1):
                                data = span.text

                                # Include into dict
                                all_data[label] = data

                                # Erase it
                                label = ""
                                data = ""

    return all_data







    
if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    THE_BAR = WaitingBar('[*] Downloading...')
    bla = get_specific_data("PETR4")
    print(bla)

    exit(-1)
    # lista = get_data()
    # THE_BAR.stop()

    # firebase = firebase.FirebaseApplication('https://bovespastockratings.firebaseio.com/', None)

    file_output = open('firebase.json', 'w')


    #Transform em uma lista, agora preciso passar para formato JSON
    # array_format = list(lista.items())

    # print(array_format, len(array_format))

    # Adiciona a data que esta pegando a info
    json_format = {
      "date": time.strftime("%c")
    }

    hashes_list = []
    # First include the list of all hashes
    for i in range(0, len(array_format)):
        hashes_list.append(array_format[i][1])

    stocks = []
    # Then from a list of hashes we will transform to a list of stocks
    for i in range(0, len(hashes_list)):
        for key in hashes_list[i]:
            # Adds stockCode
            hashes_list[i][key]["stockCode"] = key
            stocks.append(hashes_list[i][key])
    


#     json_format = {
#     "0": {
#         "DAGB33": {
#             "Cresc.5a": "46,43%",
#             "DY": "0,00%",
#             "Div.Brut/Pat.": "1,37",
#             "EBITDA": "4,75%",
#             "EV/EBIT": "0,00",
#             "Liq.2m.": "916.730,00",
#             "Liq.Corr.": "1,16",
#             "Mrg.Liq.": "0,38%",
#             "P/Ativ.Circ.Liq.": "0,00",
#             "P/Ativo": "0,000",
#             "P/Cap.Giro": "0,00",
#             "P/EBIT": "0,00",
#             "P/L": "0,00",
#             "P/VP": "0,00",
#             "PSR": "0,000",
#             "Pat.Liq": "9.803.230.000,00",
#             "ROE": "-0,47%",
#             "ROIC": "4,59%",
#             "cotacao": "480,00",
#             "nota": 0.5
#         }
#     }
# }


    # beautify JSON
    new_json = json.dumps(json_format, sort_keys=True, indent=4, separators=(',', ': '))

    # # transform back again in dict
    new_json = ast.literal_eval(new_json)

    # print (new_json)

    # Calculate the score of the stock
    final_stocks = []
    for stock in stocks:
        nota = 0
        patrLiq = float(stock["Pat.Liq"].replace('.', '').replace(',', '.'))
        if patrLiq > 2000000000:
            nota = nota + 1
        liqCorr = float(stock["Liq.Corr."].replace('.', '').replace(',', '.'))
        if liqCorr > 1.5:
            nota = nota + 1
        roe = float(stock["ROE"].replace('.', '').replace(',', '.').replace('%', ''))
        if roe > 20: 
            nota = nota + 1
        divPat = float(stock["Div.Brut/Pat."].replace('.', '').replace(',', '.').replace('%', ''))
        if divPat < 0.5 and divPat > 0: 
            nota = nota + 1
        cresc = float(stock["Cresc.5a"].replace('.', '').replace(',', '.').replace('%', ''))
        if cresc > 5: 
            nota = nota + 1
        pvp = float(stock["P/VP"].replace('.', '').replace(',', '.').replace('%', ''))
        if pvp < 2 and pvp > 0: 
            nota = nota + 1
        pl = float(stock["P/L"].replace('.', '').replace(',', '.').replace('%', ''))
        if pl < 15 and pl > 0: 
            nota = nota + 1
        dy = float(stock["DY"].replace('.', '').replace(',', '.').replace('%', ''))
        if dy > 2.5: 
            nota = nota + 1
        stock["nota"] = float(nota) / 8.0 * 10.0

        newStock = {}
        newStock["patrimonioLiquido"] = patrLiq
        newStock["liquidezCorrente"] = liqCorr
        newStock["ROE"] = roe
        newStock["divSobrePatrimonio"] = divPat
        newStock["crescimentoCincoAnos"] = cresc
        newStock["precoSobreVP"] = pvp
        newStock["precoSobreLucro"] = pl
        newStock["dividendos"] = dy
        newStock["stockCode"] = stock["stockCode"]
        newStock["score"] = stock["nota"]
        newStock["stockPrice"] = float(stock["cotacao"].replace('.', '').replace(',', '.'))
        newStock["PSR"] = float(stock["PSR"].replace('.', '').replace(',', '.'))
        newStock["precoSobreAtivo"] = float(stock['P/Ativo'].replace('.', '').replace(',', '.'))
        newStock["precoSobreCapitalGiro"] = float(stock['P/Cap.Giro'].replace('.', '').replace(',', '.'))
        newStock["precoSobreEBIT"] = float(stock['P/EBIT'].replace('.', '').replace(',', '.'))
        newStock["precoSobreAtivoCirculante"] = float(stock['P/Ativ.Circ.Liq.'].replace('.', '').replace(',', '.'))
        newStock["EVSobreEBIT"] = float(stock['EV/EBIT'].replace('.', '').replace(',', '.'))
        newStock["margemEBIT"] = float(stock["EBITDA"].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["margemLiquida"] = float(stock['Mrg.Liq.'].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["ROIC"] = float(stock["ROIC"].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["liquidezDoisMeses"] = float(stock['Liq.2m.'].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["timestamp"] = str(datetime.datetime.now())
        
        final_stocks.append(newStock)

        


    # # # beautify JSON
    output_json = json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': '))

    # print (output_json)

    # # # Write in the file
    file_output.write(output_json)
    file_output.close()


    # Erases firebase
    # firebase.delete('/stocks', None)
    # firebase.delete('/last_date', None)


    # result = firebase.post('/stocks', data=output_json )
    # print (result)
    # result = firebase.post('/last_date', data=time.strftime("%c"))
    # print (result)


    # Saves in mongoDB
    client = MongoClient(os.environ['MONGO_URI'])
    db = client.recentStocks
    stocks_coll = db.stocks

    # First drop the collection
    db.stocks.drop()

    for i in range(0, len(final_stocks)):
        stock = final_stocks[i]
        # Insert in mongo
        stock_id = stocks_coll.insert_one(stock).inserted_id
        print("Inserted object ", i, " of ", len(final_stocks), " :",   stock_id)
