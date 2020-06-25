import couchdb
import json
import re
import uuid

server = couchdb.Server('http://admin:password@192.168.2.211:5984/')
db = server['animes']
db_td = server['animes_td']

dados_animes = json.load(open('anihubsub/siteweb/static/animeDB/anime-offline-database.json',))

contador = 1

for info_anime in dados_animes['data']: 
    identificador = str(uuid.uuid5(uuid.NAMESPACE_DNS, info_anime['title'] + info_anime['type'] + str(info_anime['episodes'])))
    try:        
        db[str(identificador)]       
        info_anime['recomendado'] = 0
        info_anime['disponibilizar'] = 0
        db_td[identificador] = info_anime
        print('Contador = ' + str(contador) + ' -- ' + 'Titulo:' + info_anime['title'])
        contador += 1
    except:
        info_anime['recomendado'] = 0
        info_anime['disponibilizar'] = 0        
        db[identificador] = info_anime
        continue