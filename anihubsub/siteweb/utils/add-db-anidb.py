import xml.etree.ElementTree as ET
import requests
import json
import re
import urllib.request
import uuid
import couchdb
from datetime import datetime
from PIL import Image

lista_de_codigos = {
    # '14111':'https://static.tvmaze.com/uploads/images/original_untouched/256/640071.jpg',
    # '6257': 'https://static.tvmaze.com/uploads/images/original_untouched/22/55807.jpg',
    # '7525': 'https://static.tvmaze.com/uploads/images/original_untouched/22/56879.jpg',
    '13756': 'https://static.tvmaze.com/uploads/images/original_untouched/165/414677.jpg'
}

for codigo in lista_de_codigos:

# codigo = '11981'

    server = couchdb.Server('http://admin:password@192.168.2.211:5984/')
    db = server['ahs']

    raiz = ET.fromstring(requests.get("http://api.anidb.net:9001/httpapi?request=anime&client=fagnerpc&clientver=2&protover=1&aid="+codigo, verify=True).content)

    # tree = ET.parse('anihubsub/siteweb/static/animesXML/Eromangasensei.xml')
    # raiz = tree.getroot()

    #documento do CouchDB
    doc_anime = {}

    #Pega o Título Principal
    for t in raiz.find('.//titles'):
        if t.attrib['type'] == 'main':
            nome_xml = doc_anime['titulo'] = t.text

    #Pega o Período de Exibição
    doc_anime['inicio_de_exibicao'] = raiz.find('.//startdate').text
    doc_anime['final_de_exibicao'] = raiz.find('.//enddate').text

    #Pega Figura
    doc_anime['url_thumb'] = 'https://cdn-eu.anidb.net/images/main/' + raiz.find('.//picture').text
    urllib.request.urlretrieve(doc_anime['url_thumb'], 'anihubsub/siteweb/static/img/anidb/' + raiz.find('.//picture').text)

    image = Image.open('anihubsub/siteweb/static/img/anidb/' + raiz.find('.//picture').text)
    image.thumbnail((96, 400))
    image.save('anihubsub/siteweb/static/img/thumbs/' + raiz.find('.//picture').text)

    links_externos = {}
    links_mal = []
    links_ann = []

    for t in raiz.findall('resources'):
        for t2 in t.findall('resource'):          
            if t2.attrib['type'] == '1': #AnimeNetwork
                for t3 in t2.findall('externalentity'):
                    links_ann.append('https://www.animenewsnetwork.com/encyclopedia/anime.php?id='+ t3.find('identifier').text)      
            if t2.attrib['type'] == '2': #MyAnimeList
                for t3 in t2.findall('externalentity'):                
                    links_mal.append('https://myanimelist.net/anime/'+ t3.find('identifier').text) 

    links_externos['link_mal'] = links_mal
    links_externos['link_ann'] = links_ann
    links_externos['link_anidb'] = 'https://anidb.net/anime/' + codigo
    doc_anime['link_externos'] = links_externos

    identificador = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_anime['titulo']))

    doc_anime['id_anidb'] = codigo
    doc_anime['recomendado'] = 0
    doc_anime['disponibilizar'] = 0
    doc_anime['url_banner'] = lista_de_codigos[codigo]
    doc_anime['url_legendas'] = 'static/legendas/' + re.sub('[^A-Za-z0-9]+', '_', doc_anime['titulo']).lower() + '.zip'
    doc_anime['timestamp'] = datetime.timestamp(datetime.now())

    db[identificador] = doc_anime

    mydata = ET.tostring(raiz, encoding = "unicode")
    nome_xml = re.sub('[^A-Za-z0-9]+', '', nome_xml)
    myfile = open('anihubsub/siteweb/static/animesXML/'+ nome_xml + '.xml', "w")
    myfile.write(mydata)

print("Fim")