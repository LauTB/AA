from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView 
import django.contrib.auth as auth
from django.contrib.auth.views import LoginView, LogoutView
from AA.forms import RegisterForm, StudentRegistrationForm, TeacherRegistrationForm, AdministrativeRegistrationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from estudiante.models import User


# Create your views here.

class Login(LoginView):
    template_name ='index.html'

def login(request): #se va
    return render(request, 'index.html')

def register(request):#se va
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        #data = request.POST.copy()
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username = username, password = raw_password)
            auth.login(request, user)
            user_type = form.cleaned_data.get('user_type')
            return redirect_user(user_type)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def redirect_user(user_type): #se va
    if user_type == '1':
        return redirect ('estudiantes:estudiante')
    if user_type == '2':
        return redirect ('estudiantes:profesor')
    return redirect ('trab')



def signup(request):
    if request.method =='POST':
        form = None

class StudentRegistrationView(CreateView):
    form_class = StudentRegistrationForm
    template_name = 'register_estudiante.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('estudiantes:estudiante')

class TeacherRegistrationView(CreateView):
    form_class = TeacherRegistrationForm
    template_name = 'test_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('estudiantes:user_profesor')

class AdministrativeRegistrationView(CreateView):
    form_class = AdministrativeRegistrationForm
    template_name = 'base_registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'administrative'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('user')

class RegisterView(TemplateView):
    template_name = 'register_selector.html'