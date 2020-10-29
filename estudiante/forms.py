from django import forms
from estudiante.models import *
from django.contrib.auth.forms import UsernameField

class UserUpdateForm( forms.ModelForm):
    success_url = forms.CharField(widget=forms.HiddenInput(),required=False)
    username = UsernameField(required= False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)   

    field_order = ['username','first_name','last_name','email',]

    class Meta():
        model = User
        fields = ['username','first_name','last_name','email',]


class EstudianteUpdateForm(forms.ModelForm):
    class Meta():
        model = Estudiante
        fields = ('inicio', 'compatible', 'carrera', 'etapa','anno' )
        
    def save(self, user,  commit=True):
        super().save(commit=False)
        est= self.instance.Estudiante
        student = Estudiante.objects.get(user_id= user.id)
        carrera = self.cleaned_data.get('carrera')
        etapa = self.cleaned_data.get('etapa')
        anno = self.cleaned_data.get('anno')
        compatible = [self.cleaned_data.get('asignaturas_compatibles')]
        inicio= self.cleaned_data.get('inicio')
        student.carrera= carrera
        student.inicio = inicio
        student.compatible.set(compatible)
        student.etapa = etapa
        student.anno = anno
        student.user = user
        if commit:
            student.save()       
        return student

class ProfesorUpdateForm(forms.ModelForm):
    class Meta():
        model = Profesor
        fields = ('departamento', )
        
    # def save(self, user,  commit=True):
    #     super().save(commit=False)
    #     prof= self.instance.Profesor
    #     profesor = Profesor.objects.get(user_id= user.id)
    #     profesor.carrera= self.cleaned_data.get('departamento')
    #     if commit:
    #         profesor.save()       
    #     return profesor

class PlanCreateForm(forms.ModelForm):
    success_url = forms.CharField(widget=forms.HiddenInput(),required=False)
    carrera = forms.ModelChoiceField(queryset= Carrera.objects.all(), required= True)
    curso = forms.DateField(required= True)
    semestre = forms.IntegerField(min_value= 1, max_value= 2, required=True)
    evaluacion = forms.IntegerField(min_value= 2, max_value= 5, required=True)
    class Meta():
        model = PlanTrabajo
        exclude = ('tutor',)

    def save(self,user,commit=True):
        super().save(commit=False)
        profesor = Profesor.objects.get(user_id= user.id)
        estudiante = self.cleaned_data.get('estudiante')
        plan = PlanTrabajo.objects.create(tutor= profesor,
                                    evaluacion= self.cleaned_data.get('evaluacion'),
                                    semestre= self.cleaned_data.get('semestre'),
                                    curso= self.cleaned_data.get('curso'),
                                    asignatura= self.cleaned_data.get('asignatura'),
                                    estudiante= estudiante )
        
        Imparte.objects.create(estudiante= estudiante,
                             asignatura=self.cleaned_data.get('asignatura'),
                             carrera= self.cleaned_data.get('carrera'))
        return plan


class PlanUpdateForm(forms.ModelForm):
    success_url = forms.CharField(widget=forms.HiddenInput(),required=False)
    class Meta:
        model = PlanTrabajo
        fields = ['estudiante', 'asignatura','curso','semestre','evaluacion']


