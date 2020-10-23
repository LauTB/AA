from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView 
import django.contrib.auth as auth
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView
from AA.forms import StudentRegistrationForm, TeacherRegistrationForm, AdministrativeRegistrationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from estudiante.models import User


# Create your views here.

class Login(LoginView):
    template_name ='index.html'
    redirect_field_name = 'estudiantes:estudiante'
    next='estudiantes:estudiante'

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        super().post(request,args,kwargs)
        user = auth.authenticate(username= request.POST['username'], password= request.POST['password'])
        if user is None:
            return HttpResponseRedirect(reverse('login'))
        if user.is_student:
            return HttpResponseRedirect(reverse('estudiantes:estudiante'))
        if user.is_teacher:
            return HttpResponseRedirect(reverse('estudiantes:profesor'))
        if user.is_administrative:
            return HttpResponseRedirect(reverse('estudiantes:trabajador'))
            
        return HttpResponseRedirect(reverse('estudiantes:trabajador'))
        


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
    template_name = 'register_profesor.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('estudiantes:profesor')

class AdministrativeRegistrationView(CreateView):
    form_class = AdministrativeRegistrationForm
    template_name = 'base_registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'administrative'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('estudiantes:trabajador')

class RegisterView(TemplateView):
    template_name = 'register_selector.html'

# class PasswordChangeView(PasswordChangeView):
#     success_url = 'estudiantes:estudiante'