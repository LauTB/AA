from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView 
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

def login(request):
    return render(request, 'index.html')

def register(request):
    
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

def redirect_user(user_type):
    if user_type == '1':
        return redirect ('estudiantes:estudiante')
    if user_type == '2':
        return redirect ('estudiantes:profesor')
    return redirect ('user')

def user(request):
    return render(request, 'user_estudiante.html')

def signup(request):
    if request.method =='POST':
        form = None

class StudentRegistrationView(CreateView):
    form_class = StudentRegistrationForm
    template_name = 'test_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('estudiante:user_estudiante')

class TeacherRegistrationView(CreateView):
    form_class = TeacherRegistrationForm
    template_name = 'test_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('estudiante:user_profesor')

class AdministrativeRegistrationView(CreateView):
    form_class = AdministrativeRegistrationForm
    template_name = 'user_type_selection.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'administrative'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('user')