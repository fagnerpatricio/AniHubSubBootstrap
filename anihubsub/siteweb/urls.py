from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),    
    path('animes/<letra>', views.adminAnimes, name='adminAnimes'),
    path('buscaalfabetica/<letra>', views.buscaAlfabetica, name='buscaAlfabetica'),
    path('buscaanimes', views.buscaAnimes, name='buscaAnimes'),
    path('detalhesanimes/<id>', views.detalhesAnimes, name='detalhesAnimes'),
    path('salvaranimes/<path:path>', views.salvarAnimes, name='salvarAnimes'),
    path('upload/<path:path>', views.upload, name='upload'),
    path('fansubs/', views.listaDeFansubs, name='listaDeFansubs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)