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

    
if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    THE_BAR = WaitingBar('[*] Downloading...')
    lista = get_data()
    THE_BAR.stop()

    firebase = firebase.FirebaseApplication('https://bovespastockratings.firebaseio.com/', None)

    file_output = open('firebase.json', 'w')


    #Transform em uma lista, agora preciso passar para formato JSON
    array_format = list(lista.items())

    # print(array_format, len(array_format))

    # Adiciona a data que esta pegando a info
    json_format = {
      "date": time.strftime("%c")
    }

    for i in range(0, len(array_format)):
        json_format[str(array_format[i][0])] = array_format[i][1]

    # print (json_format)


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
#     },
#     "1": {
#         "ATOM3": {
#             "Cresc.5a": "0,00%",
#             "DY": "0,00%",
#             "Div.Brut/Pat.": "0,00",
#             "EBITDA": "0,00%",
#             "EV/EBIT": "-228,80",
#             "Liq.2m.": "319.438,00",
#             "Liq.Corr.": "0,00",
#             "Mrg.Liq.": "0,00%",
#             "P/Ativ.Circ.Liq.": "0,00",
#             "P/Ativo": "127,459",
#             "P/Cap.Giro": "0,00",
#             "P/EBIT": "-228,80",
#             "P/L": "-512,46",
#             "P/VP": "-9,20",
#             "PSR": "0,000",
#             "Pat.Liq": "-8.131.000,00",
#             "ROE": "1,80%",
#             "ROIC": "0,00%",
#             "cotacao": "3,58",
#             "nota": 0.375
#         }
#     }
# }


    # beautify JSON
    new_json = json.dumps(json_format, sort_keys=True, indent=4, separators=(',', ': '))

    # # transform back again in dict
    new_json = ast.literal_eval(new_json)

    # print (new_json)

    # # # Calculate the score of the stock
    # for key in new_json.keys():
    #     # print (new_json[key])
    #     if key != 'date':
    #         for stock in new_json[key]:
    #             nota = 0
    #             patrLiq = float(new_json[key][stock]["Pat.Liq"].replace('.', '').replace(',', '.'))
    #             if patrLiq > 2000000000:
    #                 nota = nota + 1
    #             liqCorr = float(new_json[key][stock]["Liq.Corr."].replace('.', '').replace(',', '.'))
    #             if liqCorr > 1.5:
    #                 nota = nota + 1
    #             roe = float(new_json[key][stock]["ROE"].replace('.', '').replace(',', '.').replace('%', ''))
    #             if roe > 20: 
    #                 nota = nota + 1
    #             divPat = float(new_json[key][stock]["Div.Brut/Pat."].replace('.', '').replace(',', '.').replace('%', ''))
    #             if divPat < 0.5 and divPat > 0: 
    #                 nota = nota + 1
    #             cresc = float(new_json[key][stock]["Cresc.5a"].replace('.', '').replace(',', '.').replace('%', ''))
    #             if cresc > 5: 
    #                 nota = nota + 1
    #             pvp = float(new_json[key][stock]["P/VP"].replace('.', '').replace(',', '.').replace('%', ''))
    #             if pvp < 2 and pvp > 0: 
    #                 nota = nota + 1
    #             pl = float(new_json[key][stock]["P/L"].replace('.', '').replace(',', '.').replace('%', ''))
    #             if pl < 15 and pl > 0: 
    #                 nota = nota + 1
    #             dy = float(new_json[key][stock]["DY"].replace('.', '').replace(',', '.').replace('%', ''))
    #             if dy > 2.5: 
    #                 nota = nota + 1
    #             new_json[key][stock]["nota"] = float(nota) / 8.0 * 10.0


                # print (stock, '>>>>>>>>>>>>>>>>>>>>>>>.',patrLiq,liqCorr,roe,divPat,cresc,pvp,pl,dy, nota)


    # # # beautify JSON
    output_json = json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': '))

    # print (output_json)

    # # # Write in the file
    file_output.write(output_json)
    file_output.close()


    result = firebase.post('/stocks', data=output_json )
    print (result)
    result = firebase.post('/last_date', data=time.strftime("%c"))
    print (result)
    
    










    # print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<14} {14:<7}'.format('Papel',
    #                                                                                                                                       'Cotação',
    #                                                                                                                                       'P/L',
    #                                                                                                                                       'P/VP',
    #                                                                                                                                       'PSR',
    #                                                                                                                                       'DY',
    #                                                                                                                                       'P/EBIT',
    #                                                                                                                                       'EV/EBIT',
    #                                                                                                                                       'EBITDA',
    #                                                                                                                                       'Mrg.Liq.',
    #                                                                                                                                       'Liq.Corr.',
    #                                                                                                                                       'ROIC',
    #                                                                                                                                       'ROE',
    #                                                                                                                                       'Div.Brut/Pat.',
    #                                                                                                                                       'Cresc.5a'))
    
    # print('-'*154)
    # for k, v in lista.items():
    #     print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<14} {14:<7}'.format(k,
    #                                                                                                                                           v['cotacao'],
    #                                                                                                                                           v['P/L'],
    #                                                                                                                                           v['P/VP'],
    #                                                                                                                                           v['PSR'],
    #                                                                                                                                           v['DY'],
    #                                                                                                                                           v['P/EBIT'],
    #                                                                                                                                           v['EV/EBIT'],
    #                                                                                                                                           v['EBITDA'],
    #                                                                                                                                           v['Mrg.Liq.'],
    #                                                                                                                                           v['Liq.Corr.'],
    #                                                                                                                                           v['ROIC'],
    #                                                                                                                                           v['ROE'],
    #                                                                                                                                           v['Div.Brut/Pat.'],
    #                                                                                                                                           v['Cresc.5a']))

