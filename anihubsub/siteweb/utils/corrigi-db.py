import couchdb
from datetime import datetime
import xml.etree.ElementTree as ET
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

server = couchdb.Server('http://admin:password@192.168.2.211:5984/')
db = server['ahs']

tree = ET.parse('anihubsub/siteweb/static/animesXML/AnimaYell.xml')
raiz = tree.getroot()

# #Adiciona Premier
# for id in db:
#     if id != '_design/ahs':
#         # print(db[documento]['inicio_de_exibicao'])
#         documento = db.get(id)
#         documento['premier'] = define_premier(documento['inicio_de_exibicao'],documento['final_de_exibicao'])
#         db.save(documento)

# #Adiciona FanSub
# for id in db:
#     if id != '_design/ahs':
#         documento = db.get(id)
#         documento['fansub'] = 'Legendas Otaku'
#         db.save(documento)

# Adiciona Episódios

documento = db.get("e4657cf9-1832-5426-a959-541b216b3e82")

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

# lista_de_nomes_de_episodios = sorted(lista_de_nomes_de_episodios, key=lambda tup: tup[0])
lista_de_nomes_de_episodios.sort(key=itemgetter(3))
documento['episodios'] = lista_de_nomes_de_episodios
documento['sinopse'] = 'O mangá gira em torno de Kohane Hatoya, uma jovem que gosta de ajudar os outros. Depois que ela se muda do primário para o ensino médio, ela fica fascinada com a torcida, e ela começa um clube de líderes de torcida em sua escola. Juntando-se a Kohane em suas atividades de animadora de torcida está o experiente amigo de infância de Hizume e Kohane, Uki.'

db.save(documento)
print(lista_de_nomes_de_episodios)
