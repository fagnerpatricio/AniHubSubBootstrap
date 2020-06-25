from django.shortcuts import render
from django.http import HttpResponse
from cloudant.client import Cloudant
from cloudant.view import View


def index(request):
    return render(request, 'index.html')

def indexBulma(request):
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
            anime['value']['thumb'],
            anime['value']['legenda'],
            anime['value']['inicio'],
            anime['value']['fim'],
            anime['value']['links']
        ))

    return render(request, 'indexBulma.html', {'animes_recomendados': dados, 'ultimos_lancamentos': dados2})

# http://192.168.2.211:5984/animes/_design/ulitmos/_view/ultimos_animes?descending=true&limit=2&include_docs=true
