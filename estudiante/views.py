from django.shortcuts import render
from django.views.generic import ListView, UpdateView 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from AA.forms import StudentRegistrationForm, TeacherRegistrationForm, AdministrativeRegistrationForm

#from apps.estudiante.forms import UserForm, EstudianteForm
from estudiante.models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')


# @login_required
# def special(request):
#     return HttpResponse("Entraste")

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))

# def estudiantes_list(request):
#     estudiante = Estudiante.objects.all()
#     context = {'estudiantes': user}
#     return render (request, 'estudiante/estudiante_list.html', context)


def user_estudiante(request):
    return render (request, 'estudiante/user_estudiante.html')

def user_profesor(request):
    return render (request, 'estudiante/user_profesor.html')

class EstudianteListView(ListView):
    model = Estudiante
    template_name = "estudiante/estudiante_list.html"

class EtapaListView(ListView):
    model = Etapa
    template_name = ".html"

class ProfesorListView(ListView):
    model = Profesor
    template_name = ".html"

class PlanTrabajoListView(ListView):
    model = PlanTrabajo
    template_name = ".html"

class ImparteListView(ListView):
    model = Imparte
    template_name = ".html"


class StudentUpdateView(UpdateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = 'test_register'
    success_url = 'estudiantes:user_estudiante'

class TeacherUpdateView(UpdateView):
    model = User
    form_class = TeacherRegistrationForm
    template_name = 'test_register'
    success_url = 'estudiantes:user_profesor'

class AdministrativeUpdateView(UpdateView):
    model = User
    form_class = AdministrativeRegistrationForm
    template_name = 'test_register'
    success_url = 'user'
