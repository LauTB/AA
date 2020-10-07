from django import forms
from apps.estudiante.models import Profesor, Estudiante, User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput())
    class Meta():
        model = Estudiante
        fields = ('usuario', 'contraseña')

class EstudianteForm(forms.ModelForm):
    class Meta():
        model = Estudiante
        fields = ('año', 'etapa')


class EstudianteUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Estudiante
        fields = ("",)
