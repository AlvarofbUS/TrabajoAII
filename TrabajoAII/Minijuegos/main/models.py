from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    #idJuego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name="idJuegoCategoria")
    logo = models.URLField(max_length=150)
    enlace = models.URLField(max_length=150)
    
    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    idSubcategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    enlace = models.URLField(max_length=150)
    #idJuego = models.ForeignKey(Juego, on_delete=models.CASCADE, verbose_name="idJuego")
    idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    #idCategoria = models.ManyToManyField('Categoria')

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    idJuego = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    imagen = models.URLField(max_length=150)
    descripcion = models.TextField()
    rating = models.CharField(max_length=10)
    numVotos = models.CharField(max_length=10)
    enlace = models.URLField(max_length=150)
    numPartidas = models.CharField(max_length=10)
    #idCategoria = models.ManyToManyField('Categoria')
    #idSubcategoria = models.ManyToManyField('SubCategoria')
    idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    idSubcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
