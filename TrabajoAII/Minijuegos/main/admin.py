from django.contrib import admin
from main.models import Juego, Categoria, Subcategoria

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Juego)