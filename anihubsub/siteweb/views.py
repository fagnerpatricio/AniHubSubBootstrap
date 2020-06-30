from django.shortcuts import render
from django.http import HttpResponse
from cloudant.client import Cloudant
from cloudant.view import View
from cloudant.query import Query
from django.core.files.storage import FileSystemStorage
from django import forms

import couchdb

alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def indexBootStrap5(request):
    return render(request, 'index.html')

def index(request):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # Create client using auto_renew to automatically renew expired cookie auth
    client = Cloudant('admin', 'password', url='http://192.168.2.211:5984', connect=True)
    db = client['ahs']
    animes_recomendados = db.get_view_result('_design/ahs', 'ani-recomendados')

    dados = []

    for anime in animes_recomendados:
        dados.append((anime['value']['titulo'],anime['value']['banner'],anime['value']['legenda']))
    
    dados2 = []
    ultimos_animes_adicionados = View(db['_design/ahs'], 'ultimos_adicionados')
    for anime in ultimos_animes_adicionados(include_docs=True, descending=True, limit=10)['rows']:
        dados2.append((
            anime['value']['titulo'],
            anime['value']['thumb'] + '.png',
            anime['value']['legenda'],
            anime['value']['inicio'],
            anime['value']['fim'],
            anime['value']['premier'],
            anime['value']['links'],
            anime['value']['fansub']
        ))

    return render(request, 'index.html', {'animes_recomendados': dados, 'ultimos_lancamentos': dados2, 'alfabeto':alfabeto})

def adminAnimes(request,letra):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    client = Cloudant('admin', 'password', url='http://192.168.2.211:5984', connect=True)
    db = client['ahs']

    busca_animes =  View(db['_design/ahs'], 'busca-alfabetica')

    lista_de_animes = [] 
    for anime in busca_animes(key=str(letra))['rows']:
        lista_de_animes.append((
            anime['value']['titulo'],
            anime['value']['banner'],
            anime['value']['legenda'],
            anime['value']['inicio'],
            anime['value']['fim'],
            anime['value']['premier'],
            anime['value']['links'],
            anime['value']['fansub']
        ))
    
    return render(request, 'adminAnimes.html', {'resultado':lista_de_animes, 'alfabeto':alfabeto})

def buscaAlfabetica(request,letra='A'):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    client = Cloudant('admin', 'password', url='http://192.168.2.211:5984', connect=True)
    db = client['ahs']

    busca_animes =  View(db['_design/ahs'], 'busca-alfabetica')

    lista_de_animes = [] 
    for anime in busca_animes(key=str(letra))['rows']:
        lista_de_animes.append((
            anime['value']['titulo'],
            anime['value']['banner'],
            anime['value']['legenda'],
            anime['value']['inicio'],
            anime['value']['fim'],
            anime['value']['premier'],
            anime['value']['links'],
            anime['value']['fansub']
        ))

    return render(request, 'buscaAlfabetica.html', {'resultado':lista_de_animes, 'alfabeto':alfabeto})

def buscaAnimes(request):
    if request.method == 'POST':
        client = Cloudant('admin', 'password', url='http://192.168.2.211:5984', connect=True)
        db = client['ahs']
       
        selector = {"titulo_pesquisa": {"$regex": request.POST.get('texto_para_pesquisa').lower()}}
        docs = db.get_query_result(selector)
        
        lista_de_animes = []
        for anime in docs:
            lista_de_animes.append((
                anime['titulo'],
                anime['url_banner'],
                anime['url_legendas'],
                anime['inicio_de_exibicao'],
                anime['final_de_exibicao'],
                anime['premier'],
                anime['link_externos'],
                anime['fansub']
            ))    
        
        return render(request, 'buscaAlfabetica.html', {'resultado':lista_de_animes, 'alfabeto':alfabeto})

def detalhesAnimes(request,id=None):
    client = Cloudant('admin', 'password', url='http://192.168.2.211:5984', connect=True)
    db = client['ahs']

    busca_animes =  View(db['_design/ahs'], 'anime-detalhes')
    
    lista_de_animes = []
    for anime in busca_animes(key=str(id))['rows']:
        lista_de_animes.append(anime['value']['titulo'])
        lista_de_animes.append(anime['value']['banner'])
        lista_de_animes.append(anime['value']['legenda'])
        lista_de_animes.append(anime['value']['inicio'])
        lista_de_animes.append(anime['value']['fim'])
        lista_de_animes.append(anime['value']['premier'])
        lista_de_animes.append(anime['value']['links'])
        lista_de_animes.append(anime['value']['fansub'])
        lista_de_animes.append(anime['value']['episodios'])
        lista_de_animes.append(anime['value']['sinopse'])
        lista_de_animes.append(anime['value']['planoDeFundo'])

    return render(request, 'detalhesAnimes.html', {'resultado':lista_de_animes, 'alfabeto':alfabeto})


def upload(request):
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
    return render(request, 'upload.html')
# http://192.168.2.211:5984/animes/_design/ulitmos/_view/ultimos_animes?descending=true&limit=2&include_docs=true
# http://192.168.2.211:5984/ahs/_design/ahs/_view/busca-alfabetica?key="A"