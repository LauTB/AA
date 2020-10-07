from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from estudiante.models import User, Estudiante, Profesor, Etapa
from asignatura.models import Asignatura, Carrera

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length= 30)
    last_name = forms.CharField(max_length= 150)
    email = forms.EmailField(max_length= 254, help_text= 'Se requiere una dirección de correo válida.')
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices= [(1, 'Alumno'), (2, 'Profesor'), (3, 'Administrativo')])

    class Meta(UserCreationForm.Meta):
        model = User
        #fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')
        if user_type == '1':
            user.is_student = True
            user.save()
        elif user_type == '2':
            user.is_teacher = True
            user.save()
        else:
            user.is_administrative = True
            user.save()
        return user

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length= 30)
    last_name = forms.CharField(max_length= 150)
    email = forms.EmailField(max_length= 250, help_text= 'Se requiere una dirección de correo válida.')
    inicio_de_ayudantia = forms.DateField() #error_messages= 'Se requiere una fecha válida.', required= False
    asignaturas_compatibles = forms.ModelMultipleChoiceField(queryset=Asignatura.objects.all(), required=False)
    carrera = forms.ModelChoiceField(queryset= Carrera.objects.all(), required= False)
    etapa = forms.ModelChoiceField(queryset= Etapa.objects.all(), required= False)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name', 'email',
                'inicio_de_ayudantia', 'asignaturas_compatibles', 'carrera', 'etapa',  )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        carrera = self.cleaned_data.get('carrera')
        inicio= self.cleaned_data.get('inicio_de_ayudantia')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print(self.cleaned_data)
        #print(carrera)
        #print(inicio)
        estudiante = Estudiante.objects.create( user=user, 
                                                inicio= self.cleaned_data.get('inicio_de_ayudantia'),
                                                carrera= carrera,
                                                etapa= self.cleaned_data.get('etapa') )
        estudiante.compatible.add(*self.cleaned_data.get('asignaturas_compatibles'))
        return user

class TeacherRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length= 30)
    last_name = forms.CharField(max_length= 150)
    email = forms.EmailField(max_length= 250, help_text= 'Se requiere una dirección de correo válida.')
    departamento = forms.CharField(max_length=250)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        profesor = Profesor.objects.create(user= user, departamento= self.cleaned_data.get('departamento'))
        return user

class AdministrativeRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length= 30)
    last_name = forms.CharField(max_length= 150)
    email = forms.EmailField(max_length= 250, help_text= 'Se requiere una dirección de correo válida.')

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_administrative = True
        user.save()
        return user

