import couchdb
import json
import re
import uuid

from joblib import Parallel, delayed

dados_animes = json.load(open('anihubsub/siteweb/static/animeDB/anime-offline-database.json',))

def process_node(info_anime):
    server = couchdb.Server('http://admin:password@192.168.2.211:5984/')
    db = server['animes']
    db_td = server['animes_td']
    identificador = str(uuid.uuid5(uuid.NAMESPACE_DNS, info_anime['title'] + info_anime['type'] + str(info_anime['episodes'])))
    try:        
        db[str(identificador)]       
        info_anime['recomendado'] = 0
        info_anime['disponibilizar'] = 0
        db_td[identificador] = info_anime
    except:
        info_anime['recomendado'] = 0
        info_anime['disponibilizar'] = 0        
        db[identificador] = info_anime   

# n_jobs=1 means: use all available cores
element_information = Parallel(n_jobs=8)(delayed(process_node)(node) for node in dados_animes['data'])