import xml.etree.ElementTree as ET
import requests
import json
import re
import urllib.request
import uuid
import couchdb
from datetime import datetime
from PIL import Image
from operator import itemgetter


def define_premier(data_inicial, data_final):
    mes_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').month
    mes_final = datetime.strptime(data_final, '%Y-%m-%d').month
    ano = datetime.strptime(data_inicial, '%Y-%m-%d').year

    if mes_inicial >= 1 and mes_final <= 3:
        return "Inverno " + str(ano)
    elif mes_inicial >= 4 and mes_final <= 6:
        return "Primavera " + str(ano)
    elif mes_inicial >= 7 and mes_final <= 9:
        return "Verão " + str(ano)
    else:
        return "Outono " + str(ano)

lista_de_codigos = [    
    (
        '34',
        'https://image.tmdb.org/t/p/original/tjbcFqW9zQlmBUB0USpJhpqASOw.jpg',
        'https://image.tmdb.org/t/p/original/2vIjTPITEoHeetz1jU4UxyHL9tg.jpg',
        'A história gira em torno da estudante Tohru Honda, que começa a viver sozinha em uma tenda depois de perder sua mãe. Ela acaba morando com os colegas Yuki e Kyo Sohma, trabalhando como dona de casa. Ela logo descobre que a família foi ligada por uma maldição relacionada ao zodíaco por séculos.'
    ),
    (
        '14111',
        'https://image.tmdb.org/t/p/original/td5dHTdzEDGmvyWEhlYMPHDTlBz.jpg',
        'https://image.tmdb.org/t/p/original/rYGowgXDECVVCbyIw3LfY8szdDl.jpg',
        'Considerado um gênio devido a ter as notas mais altas do país, Miyuki Shirogane lidera o prestigioso conselho estudantil da Academia Shuchiin como seu presidente, trabalhando ao lado do belo e rico vice-presidente Kaguya Shinomiya. Os dois são frequentemente considerados como o casal perfeito pelos alunos, apesar de não terem qualquer tipo de relacionamento romântico. No entanto, a verdade é que depois de passar tanto tempo juntos, os dois desenvolveram sentimentos um pelo outro; infelizmente, nenhum deles está disposto a confessar, pois isso seria um sinal de fraqueza. Com seu orgulho como estudantes de elite na linha, Miyuki e Kaguya embarcam em uma missão para fazer o que for necessário para obter uma confissão do outro. Através de suas travessuras diárias, a batalha do amor começa!'
    ),
    (
        '9903',
        'https://image.tmdb.org/t/p/original/x15LnCbRgRlZFnq2kQdbW9tlheZ.jpg',
        'https://image.tmdb.org/t/p/original/1OCwVMlKttkbXd9mWeqmhMOj0Ci.jpg',
        'Ichijou Raku é um garoto aparentemente normal, que mantém uma promessa desde sua infância: guardar um colar-cadeado, dado por uma garota. Raku no entanto, é filho do chefe da Yakuza, e por isso nunca teve uma vida lá muito normal. Um dia Chitoge, uma aluna transferida aparece pulando o muro e caindo por cima de Raku, o que causa estranhamento entre os dois devido à perda do colar de Raku no choque entre eles. Após dias de busca e desavenças, ambos descobrem que o futuro lhes pregou uma peça: apesar de se detestarem, precisarão se fingir de namorados para evitar a guerra entre a Yakuza, da família de Raku, e a máfia, da família de Chitoge. Um romance fadado ao desastre e guerra entre facções inimigas.'
    ),
    (
        '10859',
        'https://image.tmdb.org/t/p/original/11wlRUHmAClOWPclwKiEVK8u0zj.jpg',
        'https://image.tmdb.org/t/p/original/wREvAqVPttTfW1KP2Aifd7QNjCB.jpg',
        'Ichijou Raku é um garoto aparentemente normal, que mantém uma promessa desde sua infância: guardar um colar-cadeado, dado por uma garota. Raku no entanto, é filho do chefe da Yakuza, e por isso nunca teve uma vida lá muito normal. Um dia Chitoge, uma aluna transferida aparece pulando o muro e caindo por cima de Raku, o que causa estranhamento entre os dois devido à perda do colar de Raku no choque entre eles. Após dias de busca e desavenças, ambos descobrem que o futuro lhes pregou uma peça: apesar de se detestarem, precisarão se fingir de namorados para evitar a guerra entre a Yakuza, da família de Raku, e a máfia, da família de Chitoge. Um romance fadado ao desastre e guerra entre facções inimigas.'
    )
]

# lista_de_codigos = {
#     # '14111':'https://static.tvmaze.com/uploads/images/original_untouched/256/640071.jpg',
#     # '6257': 'https://static.tvmaze.com/uploads/images/original_untouched/22/55807.jpg',
#     # '7525': 'https://static.tvmaze.com/uploads/images/original_untouched/22/56879.jpg',
#     # '13756': 'https://static.tvmaze.com/uploads/images/original_untouched/165/414677.jpg'
#     '9903': 'https://artworks.thetvdb.com/banners/posters/275670-1.jpg',
#     '10859': 'https://artworks.thetvdb.com/banners/posters/275670-2.jpg'
# }

for codigo in lista_de_codigos:

# codigo = '11981'

    server = couchdb.Server('http://admin:1234@192.168.2.180:5984/')
    db = server['ahs']

    raiz = ET.fromstring(requests.get("http://api.anidb.net:9001/httpapi?request=anime&client=fagnerpc&clientver=2&protover=1&aid="+codigo[0], verify=True).content)

    # tree = ET.parse('anihubsub/siteweb/static/animesXML/Eromangasensei.xml')
    # raiz = tree.getroot()

    #documento do CouchDB
    doc_anime = {}

    #Pega o Título Principal
    for t in raiz.find('.//titles'):
        if t.attrib['type'] == 'main':
            nome_xml = doc_anime['titulo'] = t.text
            nome_xml = doc_anime['titulo_pesquisa'] = t.text.lower()

    #Pega o Período de Exibição
    doc_anime['inicio_de_exibicao'] = raiz.find('.//startdate').text
    doc_anime['final_de_exibicao'] = raiz.find('.//enddate').text
    doc_anime['premier'] = define_premier(doc_anime['inicio_de_exibicao'],doc_anime['final_de_exibicao'])

    #Figuras
    doc_anime['url_banner'] = codigo[1]
    doc_anime['url_plano_de_fundo'] = codigo[2]    

    urllib.request.urlretrieve(doc_anime['url_banner'], 'anihubsub/siteweb/static/img/banners-animes/' + codigo[0] + '.png')
    urllib.request.urlretrieve(doc_anime['url_plano_de_fundo'], 'anihubsub/siteweb/static/img/planos-de-fundo/' + codigo[0] + '.png')

    image = Image.open('anihubsub/siteweb/static/img/banners-animes/' + codigo[0] + '.png')
    image.thumbnail((96, 400))
    image.save('anihubsub/siteweb/static/img/thumbs/' + codigo[0] + '.png')

    # #Pega Figura
    # doc_anime['url_thumb'] = 'https://cdn-eu.anidb.net/images/main/' + raiz.find('.//picture').text    
    # urllib.request.urlretrieve(doc_anime['url_thumb'], 'anihubsub/siteweb/static/img/anidb/' + raiz.find('.//picture').text)

    # image = Image.open('anihubsub/siteweb/static/img/anidb/' + raiz.find('.//picture').text)
    # image.thumbnail((96, 400))
    # image.save('anihubsub/siteweb/static/img/thumbs/' + raiz.find('.//picture').text)

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
    links_externos['link_anidb'] = ['https://anidb.net/anime/' + codigo[0]]
    doc_anime['link_externos'] = links_externos

    lista_de_nomes_de_episodios = []
    lista_de_nomes_de_ovas = []
    for episodio in raiz.iter("episode"):
        for titulo in episodio.findall('title'):
            if titulo.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == 'en':
                try:
                    lista_de_nomes_de_episodios.append((
                        str(int(episodio.find("epno").text)),
                        titulo.text,
                        episodio.find('length').text,
                        episodio.find('airdate').text
                    ))
                except:
                    lista_de_nomes_de_ovas.append('#' + episodio.find("epno").text + ' - ' + titulo.text)

    lista_de_nomes_de_episodios.sort(key=itemgetter(3))
    doc_anime['episodios'] = lista_de_nomes_de_episodios

    doc_anime['id_anidb'] = codigo[0]
    doc_anime['recomendado'] = 0
    doc_anime['disponibilizar'] = 0
    doc_anime['fansub'] = 'Legendas Otaku'
    doc_anime['sinopse'] = codigo[3]
    doc_anime['url_legendas'] = re.sub('[^A-Za-z0-9]+', '_', doc_anime['titulo']).lower() + '.zip'
    doc_anime['timestamp'] = datetime.timestamp(datetime.now())

    identificador = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_anime['titulo']))
    db[identificador] = doc_anime

    mydata = ET.tostring(raiz, encoding = "unicode")
    nome_xml = re.sub('[^A-Za-z0-9]+', '_', nome_xml)
    myfile = open('anihubsub/siteweb/static/animesXML/'+ nome_xml + '.xml', "w")
    myfile.write(mydata)

print("Fim")

# d = '2010-03-01'
# if datetime.strptime(d,'%Y-%m-%d').month >= 10 and datetime.strptime(d,'%Y-%m-%d').month <=12