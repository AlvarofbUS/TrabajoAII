from main.models import Categoria, Subcategoria, Juego
from whoosh.index import open_dir


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
            if (int(row['idSubcategoria']) >1000):
                lista.append(Juego(idJuego=row['idJuego'], titulo=row['titulo'], imagen=row['imagen'], descripcion=row['descripcion'],
                rating=row['rating'], numVotos=row['numVotos'], enlace=row['enlace'], numPartidas=row['numPartidas'],
                idCategoria=idCategoria))
            else:
                idSubcategoria = Subcategoria.objects.get(idSubcategoria=row['idSubcategoria'])
                lista.append(Juego(idJuego=row['idJuego'], titulo=row['titulo'], imagen=row['imagen'], descripcion=row['descripcion'],
                rating=row['rating'], numVotos=row['numVotos'], enlace=row['enlace'], numPartidas=row['numPartidas'],
                idCategoria=idCategoria, idSubcategoria=idSubcategoria))
    Juego.objects.bulk_create(lista)
    print('Juegos insertados: ' + str(Juego.objects.count()))
    print('--------------------------------------------------')
