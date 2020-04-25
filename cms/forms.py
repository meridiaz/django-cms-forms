from django import forms

from .models import Contenido, Comentario
from django.utils import timezone

class ContenidoForm(forms.ModelForm):

    #le decimos que modelo va a ser usado para hacer este formulario
    class Meta:
        model = Contenido
        fields = ('clave', 'valor',)


class ComentarioForm(forms.ModelForm):
    #fecha = Field(required=False,
                    #widget=forms.HiddenInput)
    #le decimos que modelo va a ser usado para hacer este formulario
    class Meta:
        model = Comentario
        fields = ('titulo', 'cuerpo',)
