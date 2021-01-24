from django.shortcuts import render

from bs4 import BeautifulSoup
import urllib.request

import os
from whoosh import qparser
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.fields import TEXT, ID, NUMERIC, Schema

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db.models import Avg, Count
from django.conf import settings

from main.models import Categoria, Subcategoria, Juego


def index(request):
    return render(request, 'index.html', {'STATIC_URL': settings.STATIC_URL})


def extraer_datos():
    main_directory = 'main/info'
    
    categoria_directory = main_directory + '/' + 'categoria'
    subcategoria_directory = main_directory + '/' + 'subcategoria'
    juegos_directory = main_directory + '/' + 'juegos'

    if not os.path.exists(main_directory):
        os.mkdir(main_directory)
    if not os.path.exists(categoria_directory):
        os.mkdir(categoria_directory)
    if not os.path.exists(subcategoria_directory):
        os.mkdir(subcategoria_directory)
    if not os.path.exists(juegos_directory):
        os.mkdir(juegos_directory)
    
    ix1 = create_in(categoria_directory, schema = schemaCategoria())
    ix2 = create_in(subcategoria_directory, schema = schemaSubcategoria())
    ix3 = create_in(juegos_directory, schema = schemaJuego())
    writer1 = ix1.writer()
    writer2 = ix2.writer()
    writer3 = ix3.writer()
    # Diccionario con las distintas categorias y sus subcategorias
    dicCateg = {}
    # Diccionario que relaciona el nombre de la categoria con su enlace
    dicNombreEnlace = {}
    # Diccionario que relaciona el enlace con su logo
    dicEnlaceLogo = {}
    # Lista que posee todos los enlaces de las categorias posibles
    todas = []
    # Diccionario id Categoria:enlace
    dicEnlaceIdCateg = {}
    # Diccionario id Subcategoria:enlace
    dicEnlaceIdSubcateg = {}
    #Diccionario enlace subcategoria:idCategoria
    dicEnlaceSubcategIdCateg = {}
    # Lista de las categorias
    enlace_categorias = []
    
    # Lista de las subcategorias
    enlace_subcategorias = []

    count_categoria = 1
    count_subcategoria = 1
    count_juego = 1
    
    f = urllib.request.urlopen('https://www.minijuegos.com/')
    s = BeautifulSoup(f, 'lxml')

    # Obtenemos categoria y sus subcategorias. Cálculo de los diccionarios y lista anteriores. 
    for i in range(1, 11):
        div = s.find('nav', class_='categories-nav').find('li', class_='js-nav-item nav-item js-nav-item-cat-'+str(i))
        enlace = div.a['href']
        nombre = div.a['title']
        f1 = urllib.request.urlopen(enlace)
        s1 = BeautifulSoup(f1, 'lxml')
        cabecera = s1.find('section', class_='full-container cat-top-games').find('div', class_='col col-11 pb-10 mt-20') if s1.find('section', class_='full-container cat-top-games') is not None else None
        if cabecera is not None:
            logo = cabecera.img['src'] if cabecera.img['src'] is not None and cabecera.img is not None else None
            dicEnlaceLogo[enlace] = logo
        
        enlace_categorias.append(enlace)
        dicEnlaceIdCateg[enlace] = count_categoria
        writer1.add_document(idCategoria = count_categoria, enlace = enlace, nombre = nombre, logo = logo)

        # Calculo las subcategorias de la categoria
        div2 = div.find('ul', class_='nav-item-level nav-item-level-2').find_all('li')
        todas.append(enlace)
        secundarias = []
        dicNombreEnlace[nombre] = enlace
        for d in div2:
            secund = d.a['href']
            nombre_secund = d.a['title']
            secundarias.append(secund)
            todas.append(secund)
            dicNombreEnlace[nombre_secund] = secund
            dicEnlaceIdSubcateg[secund] = count_subcategoria
            enlace_subcategorias.append(secund)
            writer2.add_document(idSubcategoria = count_subcategoria, nombre = nombre_secund, enlace = secund, idCategoria = count_categoria)
            count_subcategoria = count_subcategoria + 1
            dicEnlaceSubcategIdCateg[secund] = count_categoria

        dicCateg[enlace] = secundarias
        count_categoria = count_categoria + 1

    div = s.find('nav', class_='categories-nav').find('li', class_= 'js-nav-item nav-item js-nav-item-cat-8780')
    enlace = div.a['href']
    nombre = div.a['title']
    f1 = urllib.request.urlopen(enlace)
    s1 = BeautifulSoup(f1, 'lxml')
    cabecera = s1.find('section', class_='full-container cat-top-games').find('div', class_='col col-11 pb-10 mt-20') if s1.find('section', class_='full-container cat-top-games') is not None else None
    if cabecera is not None:
        logo = cabecera.img['src'] if cabecera.img['src'] is not None and cabecera.img is not None else None
        dicEnlaceLogo[enlace] = logo
        writer1.add_document(idCategoria = count_categoria, enlace = enlace, nombre = nombre, logo = logo)
    dicNombreEnlace[nombre] = enlace
    todas.append(enlace)
    dicEnlaceIdCateg[enlace] = count_categoria
    enlace_categorias.append(enlace)
    # Calculo las subcategorias de la categoria
    div2 = div.find('ul', class_='nav-item-level nav-item-level-2').find_all('li')
    secundarias = []
    for d in div2:
        secund = d.a['href']
        nombre_secund = d.a['title']
        secundarias.append(secund)  
        todas.append(secund)  
        dicNombreEnlace[nombre_secund] = secund
        dicEnlaceIdSubcateg[secund] = count_subcategoria
        enlace_subcategorias.append(secund)
        writer2.add_document(idSubcategoria = count_subcategoria, nombre = nombre_secund, enlace = secund, idCategoria = count_categoria)
        dicEnlaceSubcategIdCateg[secund] = count_categoria
        count_subcategoria = count_subcategoria + 1
    dicCateg[enlace] = secundarias
    #count_categoria = count_categoria + 1 No hace falta dado que solo hay un li de este tipo

    print('Se han indexado ' + str(count_categoria-1) + ' categorias')
    print('---------------------------------------------------------')
    print('Se han indexado ' + str(count_subcategoria-1) + ' subcategorias')
    print('---------------------------------------------------------')
    i = 0
    # Por cada una de las categorias posibles
    for l in todas:
        f1 = urllib.request.urlopen(l)
        s1 = BeautifulSoup(f1, 'lxml')
    
        juegos = s1.find('section', class_='full-container cat-games').find('div', class_='row-full').find_all('li')
        for juego in juegos:
            #Enlace, titulo e imagen del juego
            enlace = juego.find('a', class_='media')['href'] if juego.find('a', class_='media') is not None else None
            titulo = juego.find('a', class_='media')['title'] if juego.find('a', class_='media') is not None and enlace is not None else None
            imagen = juego.find('a', class_='media').img['src'] if juego.find('a', class_='media') is not None and juego.find('a', class_='media').img is not None and enlace is not None else None 
            if enlace is not None:
                f2 = urllib.request.urlopen(enlace)
                s2 = BeautifulSoup(f2, 'lxml')
                
                cabeceraJuego = s2.find('section', id='game-info')
                if cabeceraJuego is not None:
                    #Valoración, número de partidas y número de votos del juego
                    rating = cabeceraJuego.find('div', class_='rating mb-10').find('div', class_='meter-svg')['value']
                    # Colocado el siguiente if pq hay juegos que no permiten coger solo las partidas asi que omitimos esos
                    numPartidas = cabeceraJuego.find('div', class_='hgroup push-l').p.string.strip() if s2.find('div', id='contentWrapper') else None
                    numTotalVotos = cabeceraJuego.find('div', class_='game-options-buttons').find('div', class_='rating').find('span', class_='js-total-votes').string.strip()
               
                    informacion = s2.find('div', id='contentWrapper').find('div', class_='row-full').find('div', class_='col col-10').find_all('div',  {'class': 'row'})  if s2.find('div', id='contentWrapper') is not None else None
                
                    if informacion is not None:
                        bloque_descripcion = informacion[1]
                        # Descripción
                        descripcion = bloque_descripcion.find('div', class_='description group rich-html-desc xl-desc').get_text().strip()
                        # Creamos estos ids para obtener los reales según el caso
                        idCategoria = 0
                        # A partir de 1001 pondré los juegos que estén en categoria y no subcategoria
                        idSubcategoria = 1000
                        if(l in enlace_categorias):
                            idCategoria = dicEnlaceIdCateg.get(l)
                            idSubcategoria = idSubcategoria + 1
                        else:
                            #idCategoria = getIdCategoriaByEnlaceSubcategoria(l)
                            idCategoria = dicEnlaceSubcategIdCateg.get(l)
                            idSubcategoria = dicEnlaceIdSubcateg.get(l)
                        
                        writer3.add_document(idJuego = count_juego, enlace = enlace, titulo = titulo, imagen = imagen, rating = rating, numPartidas = numPartidas, numVotos = numTotalVotos, descripcion = descripcion, idCategoria = idCategoria, idSubcategoria = idSubcategoria)
                        count_juego = count_juego + 1
                        i = i + 1
                        print(count_juego)
                        if i == 3: 
                            i = 0
                            break
            break
    writer1.commit()
    writer2.commit()
    writer3.commit()
    print('Se han indexado ' + str(count_juego-1) + ' juegos')
    print('---------------------------------------------------------')


def schemaCategoria():
    schema = Schema(
        idCategoria = NUMERIC(stored=True),
        nombre = TEXT(stored=True),
        logo = TEXT(stored=True),
        enlace = TEXT(stored=True))
    return schema


def schemaSubcategoria():
    schema = Schema(
        idSubcategoria = NUMERIC(stored=True),
        nombre = TEXT(stored=True),
        enlace = TEXT(stored=True),
        idCategoria = NUMERIC(stored=True)
    )
    return schema


def schemaJuego():
    schema = Schema(
        idJuego = NUMERIC(stored=True),
        titulo = TEXT(stored=True),
        imagen = TEXT(stored=True),
        descripcion = TEXT(stored=True),
        rating = TEXT(stored=True),
        numVotos = TEXT(stored=True),
        enlace = TEXT(stored=True),
        numPartidas = TEXT(stored=True),
        idCategoria = NUMERIC(stored=True),
        idSubcategoria = NUMERIC(stored=True)
    )
    return schema


def getIdCategoriaByEnlaceSubcategoria(enlace):
    main_directory = 'main/info'
    subcategoria_directory = main_directory + '/' + 'subcategoria'
    ix = open_dir(subcategoria_directory)
    with ix.searcher() as searcher:
        entry = str(enlace)
        query = QueryParser('enlace', ix.schema).parse(entry)
        results = searcher.search(query)
        row = results[3]
        id = row['idCategoria']
    return id

'''
@login_required(login_url='/ingresar')
def populateWhoosh(request):
    print('-------------------------------------------------')
    extraer_datos()
    logout(request)
    return(HttpResponseRedirect('/index'))
'''

#@login_required(login_url='/ingresar_whoosh')
def populateWhoosh(request):
    print('---------------------------------------------------------')
    extraer_datos()
    logout(request)
    return(HttpResponseRedirect('/index'))

#@login_required(login_url='/ingresar')
def populateDjango(request):
    print('-------------------------------------------------')
    populate_categoria()
    populate_subcategoria()
    populate_juegos()
    logout(request)
    return(HttpResponseRedirect('/index'))


def ingresar(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect(''))
    formulario = AuthenticationForm()
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username = usuario, password = clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect(''))
            else:
                return (HttpResponse('<html><body> Error: usuario no activo </body></html>'))
        else:
            return (HttpResponse('<html><body><b>Error: usuario o contrase&ntilde;a incorrectos</b><br><a href=/index>Volver a la página principal</a></body></html>'))
    
    return render(request, 'ingresar.html', {'formulario':formulario})

'''
def ingresarWhoosh(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect('/populate_whoosh'))
    formulario = AuthenticationForm()
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate_whoosh'))
            else:
                return (HttpResponse('<html><body>Error: usuario no activo </body></html>'))
        else:
            return (HttpResponse('<html><body><b>Error: usuario o contrase&ntilde;a incorrectos</b><br><a href=/index>Volver a la página principal</a></body></html>'))

    return render(request, 'ingresar_whoosh.html', {'formulario': formulario})


def ingresarDjango(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect('/populate_django'))
    formulario = AuthenticationForm()
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        print(clave)
        print(usuario)
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate_django'))
            else:
                return (HttpResponse('<html><body>Error: usuario no activo </body></html>'))
        else:
            return (HttpResponse('<html><body><b>Error: usuario o contrase&ntilde;a incorrectos</b><br><a href=/index>Volver a la página principal</a></body></html>'))

    return render(request, 'ingresar_django.html', {'formulario': formulario})
'''

def populate_categoria():
    print('Cargando categorias...')
    Categoria.objects.all().delete()
    main_directory = 'main/info'
    categoria_directory = main_directory + '/' + 'categoria'
    lista = []
    ix = open_dir(categoria_directory)
    with ix.searcher() as searcher:
        doc = searcher.documents()
        for row in doc:
            lista.append(Categoria(idCategoria=row['idCategoria'], nombre=row['nombre'], 
            logo=row['logo'], enlace=row['enlace']))
    Categoria.objects.bulk_create(lista)
    print('Categorias insertadas: ' + str(Categoria.objects.count()))
    print('------------------------------------------------')


def populate_subcategoria():
    print('Cargando subcategorias...')
    Subcategoria.objects.all().delete()
    main_directory = 'main/info'
    subcategoria_directory = main_directory + '/' + 'subcategoria'
    lista = []
    ix = open_dir(subcategoria_directory)
    with ix.searcher() as searcher:
        doc = searcher.documents()
        for row in doc:
            idCategoria = Categoria.objects.get(idCategoria=row['idCategoria'])
            lista.append(Subcategoria(idSubcategoria=row['idSubcategoria'], nombre=row['nombre'],
             enlace=row['enlace'], idCategoria=idCategoria))
    Subcategoria.objects.bulk_create(lista)
    print('Subcategorias insertadas: ' + str(Subcategoria.objects.count()))
    print('-------------------------------------------------')


def populate_juegos():
    print('Cargando juegos...')
    Juego.objects.all().delete()
    main_directory = 'main/info'
    juegos_directory = main_directory + '/' + 'juegos'
    lista = []
    ix = open_dir(juegos_directory)
    with ix.searcher() as searcher:
        doc = searcher.documents()
        for row in doc:
            idCategoria = Categoria.objects.get(idCategoria=row['idCategoria'])
            idSubcategoria = Subcategoria.objects.get(idSubcategoria=row['idSubcategoria'])
            lista.append(idJuego=row['idJuego'], titulo=row['titulo'], imagen=row['imagen'], descripcion=row['descripcion'],
                rating=row['rating'], numVotos=row['numVotos'], enlace=row['enlace'], numPartidas=row['numPartidas'],
                idCategoria=idCategoria, idSubcategoria=idSubcategoria)
    Juego.objects.bulk_create(lista)
    print('Juegos insertados: ' + str(Juego.objects.count()))
    print('--------------------------------------------------')

'''
def getCategoriaByNombre(request):
    formulario =  

'''