"""Minijuegos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index', views.index),
    path('populate_django/', views.populateDjango),
    path('populate_whoosh/', views.populateWhoosh),
    path('ingresar/', views.ingresar),
    path('registrar/', views.registrar),
    path('logout', views.logout),
    path('listaCategoria/', views.listaCategoria),
    path('listaSubcategoria/<int:idCategoria>', views.getSubcategoriaByIdCategoria),
    path('juegosCategoria/<int:idCategoria>', views.getJuegosCategoriaByIdCategoria),
    path('juegosSubcategoria/<int:idSubcategoria>', views.getJuegosSubcategoriaByIdSubcategoria),
    path('juego/<int:idJuego>', views.getInformacionJuegoByIdJuego),
    path('busquedaCategoria', views.getCategoriaByName),
    path('busquedaSubcategoria', views.getSubcategoriaByName),
    path('busquedaJuego', views.getJuegoByName),
    ]
