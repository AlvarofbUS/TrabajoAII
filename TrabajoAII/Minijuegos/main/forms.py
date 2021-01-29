from django import forms

class CategoriaForm(forms.Form):
    nombreCategoria = forms.CharField(label="Nombre de la categoria", widget=forms.TextInput, required=True)

class SubcategoriaForm(forms.Form):
    nombreSubcategoria = forms.CharField(label="Nombre de la subcategoria", widget=forms.TextInput, required=True)

class JuegoForm(forms.Form):
    tituloJuego = forms.CharField(label="Titulo del juego", widget=forms.TextInput, required=True)