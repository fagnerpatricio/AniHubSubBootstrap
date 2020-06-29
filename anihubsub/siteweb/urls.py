from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bulma', views.indexBulma, name='indexBulma'),
    path('animes/<letra>', views.adminAnimes, name='adminAnimes'),
    path('buscaalfabetica/<letra>', views.buscaAlfabetica, name='buscaAlfabetica'),
    path('detalhesanimes', views.detalhesAnimes, name='detalhesAnimes'),
    path('upload', views.upload, name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)