from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import template
from cloudant.client import Cloudant
from cloudant.view import View
from cloudant.query import Query
from django.core.files.storage import FileSystemStorage
from django import forms
from operator import itemgetter
import os
import couchdb

alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

#Dados Banco de Dados
URL = 'http://192.168.2.180:5984'
USUARIO_DB = 'admin'
SENHA_DB = '1234'

lista_resultados = lambda y: [list(x['value'].values()) for x in y]
mudarAtributoInt = lambda x: 1 if x else 0


def index(request):
    db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs']
    ultimos_animes_adicionados = View(db['_design/ahs'], 'ultimos_adicionados')
   
    #Cria Contexto de retorno
    contexto = {}
    contexto['animes_recomendados'] = db.get_view_result('_design/ahs', 'ani-recomendados')
    contexto['ultimos_lancamentos'] = ultimos_animes_adicionados(include_docs=True, descending=True, limit=10)['rows']
    contexto['alfabeto'] = alfabeto

    return render(request, 'index.html', contexto)    


def adminAnimes(request,letra='A'):
    db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs']

    busca_animes =  View(db['_design/ahs'], 'busca-alfabetica')    
    lista_de_animes = lista_resultados(busca_animes(key=str(letra))['rows'])

    #Verifica se existe legenda para o anime
    for i , anime in enumerate(lista_de_animes):
        lista_de_animes[i].append(os.path.exists('anihubsub/siteweb/static/legendas/' + anime[3]))
    
    #Cria Contexto de retorno
    contexto = {}
    contexto['resultado'] = lista_de_animes
    contexto['alfabeto'] = alfabeto

    return render(request, 'adminAnimes.html', contexto)


def salvarAnimes(request,path='/animes/A'):
    if request.method == 'POST':
        db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs']

        doc = db[request.POST.get('id')]
        doc['recomendado'] = mudarAtributoInt(request.POST.get('recomendar_anime'))
        doc['disponibilizar'] = mudarAtributoInt(request.POST.get('disponibilizar_anime'))        
        doc['fansub'] = request.POST.get('fansub')
        doc.save()

    return  redirect(path)


def buscaAlfabetica(request,letra='A'):
    db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs']

    busca_animes =  View(db['_design/ahs'], 'busca-alfabetica')
   
    contexto = {}
    contexto['resultado'] = busca_animes(key=str(letra))['rows']
    contexto['alfabeto'] = alfabeto

    return render(request, 'buscaAlfabetica.html', contexto)


def buscaAnimes(request):
    if request.method == 'POST':
        db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs']
      
        selector = {"titulo_pesquisa": {"$regex": request.POST.get('texto_para_pesquisa').lower()}}        

        contexto = {}        
        contexto['resultado'] = db.get_query_result(selector)
        contexto['alfabeto'] = alfabeto  

        return render(request, 'buscaPorNomes.html', contexto)


def detalhesAnimes(request,id=None):
    db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs']

    busca_animes =  View(db['_design/ahs'], 'anime-detalhes')

    contexto = {}
    contexto['anime'] = busca_animes(key=str(id))['rows'][0]
    contexto['alfabeto'] = alfabeto

    return render(request, 'detalhesAnimes.html', contexto)


def upload(request, path='/animes/A'):
    contexto = {}
    if request.method == 'POST':        
        fs = FileSystemStorage()
        contexto['nome_arquivo_salvo'] = fs.save(request.POST.get('nome_legenda'), request.FILES['legenda'])        

    return redirect(path, contexto)


def listaDeFansubs(request):
    #Conexão Com o Banco de Dados
    db = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)['ahs_fansubs']    
    
    #Lista o Fansubs Cadastrados
    busca_fansubs =  View(db['_design/ahs_fansubs'], 'mostra-todos')        
    lista_de_fansubs = lista_resultados(busca_fansubs()['rows'])

    #Ordena pelo título
    lista_de_fansubs.sort(key=itemgetter(1))

    #Cria Contexto de resposta
    contexto = {} 
    contexto['alfabeto'] = alfabeto
    contexto['listaDeFansubs'] = lista_de_fansubs

    return render(request, 'listaDeFansubs.html', contexto)  






# client = Cloudant(USUARIO_DB, SENHA_DB, url=URL, connect=True)
# db = client['ahs']

# lista_resultados_da_busca = lambda y: [list(x.values()) for x in y]

# http://192.168.2.211:5984/animes/_design/ulitmos/_view/ultimos_animes?descending=true&limit=2&include_docs=true
# http://192.168.2.211:5984/ahs/_design/ahs/_view/busca-alfabetica?key="A"