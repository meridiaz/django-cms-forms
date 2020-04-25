from django import forms

from .models import Contenido

class ContenidoForm(forms.ModelForm):

    #le decimos que modelo va a ser usado para hacer este formulario
    class Meta:
        model = Contenido
        fields = ('clave', 'valor',)
