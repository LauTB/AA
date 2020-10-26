from django.shortcuts import render,get_object_or_404 
from django.views.generic import ListView, UpdateView , TemplateView,CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView
from django.contrib.auth.views import PasswordChangeView

from estudiante.forms import *
from estudiante.models import *
from estudiante.filters import *
from estudiante.decorators.permission import role_permission
from estudiante.customs.auth_views import AuthListView, AuthDeleteView, AuthUpdateView
# Create your views here.

@role_permission('Estudiante',False)
def user_estudiante(request):
    return render (request, 'estudiante/user_estudiante.html')

@role_permission('Profesor',False)
def user_profesor(request):
    return render (request, 'estudiante/user_profesor.html')

@role_permission('Trabajador',False)
def user_administrative(request):
    return render (request, 'estudiante/user_administrative.html')



class EstudianteUpdateView(UpdateView):
    model = User
    fields= ('username','first_name','last_name', 'email',)
    template_name = "estudiante/estudiante_edit.html"
    success_url = 'estudiantes:estudiante'
    next = 'estudiante/user_estudiante'

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context
    
    @role_permission('Estudiante')
    def get(self, request, *args, **kwargs):
        student = kwargs.pop('estudiante','')
        user_object = request.user
        user = User.objects.filter(username= user_object).get()
        user_form = UserUpdateForm()
        student = Estudiante.objects.get(user_id= request.user.id)
        student_form = EstudianteUpdateForm(instance=student)
        context = self.get_context(form1=student_form,form2=user_form)
        return render(request,self.template_name,context=context)

    @role_permission('Estudiante')
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        student = Estudiante.objects.get(user_id= request.user.id)
        user_form = UserUpdateForm(request.POST)
        student_form = EstudianteUpdateForm(request.POST)
        student_form.instance.Estudiante = student
        
        if user_form.is_valid() and student_form.is_valid():
            user_form.save(user)
            student=student_form.save(user)
            return  HttpResponseRedirect(reverse(self.success_url))
        else:
            context = self.get_context(form1=student_form,form2=user_form)
            return render(request,self.template_name,context=context)

class ProfesorUpdateView(UpdateView):
    model = User
    fields= ('username','first_name','last_name', 'email',)
    template_name = "estudiante/profesor_edit.html"
    success_url = 'estudiantes:profesor'
    next = 'estudiante/user_profesor'

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    @role_permission('Profesor')
    def get(self, request, *args, **kwargs):
        profesor = kwargs.pop('profesor','')
        user_object = request.user
        user = User.objects.filter(username= user_object).get()
        user_form = UserUpdateForm(instance=user)
        profesor = Profesor.objects.get(user_id= request.user.id)
        profesor_form = ProfesorUpdateForm(instance=profesor)
        context = self.get_context(form1=profesor_form,form2=user_form)
        return render(request,self.template_name,context=context)

    @role_permission('Profesor')
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        profesor = Profesor.objects.get(user_id= request.user.id)
        user_form = UserUpdateForm(request.POST)
        profesor_form = ProfesorUpdateForm(request.POST)
        profesor_form.instance.Profesor = profesor
        
        if user_form.is_valid() and profesor_form.is_valid():
            user_form.save(user)
            profesor= profesor_form.save(user)
            return  HttpResponseRedirect(reverse(self.success_url))
        else:
            context = self.get_context(form1=profesor_form,form2=user_form)
            return render(request,self.template_name,context=context)

class AdministrativeUpdateView(UpdateView):
    model = User
    form = UserUpdateForm
    template_name = "estudiante/administrative_edit.html"
    success_url = 'estudiantes:trabajador'
    next = 'estudiante/user_profesor'

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    @role_permission('Trabajador')
    def get(self, request, *args, **kwargs):
        user_object = request.user
        user = User.objects.filter(username= user_object).get()
        user_form = UserUpdateForm()
        context = self.get_context(form1= user_form)
        return render(request,self.template_name,context=context)

    @role_permission('Trabajador')
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        user_form = UserUpdateForm(request.POST)        
        if user_form.is_valid():
            user_form.save(user)
            return  HttpResponseRedirect(reverse(self.success_url))
        else:
            context = self.get_context(form1=user_form)
            return render(request,self.template_name,context=context)

class PasswordChangeView( PasswordChangeView):
    template_name = "estudiante/password_change.html"
    success_url = reverse_lazy('login')


class PlanTrabajoListView(ListView):
    model = PlanTrabajo
    template_name = "plan_trabajo/profesor_plan_trabajo.html"

    def get_queryset(self):
        return PlanTrabajo.objects.filter(tutor_id= self.kwargs['pk'])

class PlanTrabajoCreateView(CreateView):
    model = PlanTrabajo
    fields = '__all__'
    form = PlanCreateForm
    template_name = "plan_trabajo/profesor_add_plan.html"
    success_url = 'estudiantes:profesor'

    def get_context(self,**kwargs):
        context = {}
        context.update(kwargs)
        return context

    @role_permission("Profesor")
    def get(self, request, *args, **kwargs):
        user_object = request.user
        user = User.objects.filter(username= user_object).get()
        plan = PlanCreateForm()
        context = self.get_context(form1=plan,)
        return render(request,self.template_name,context=context)

    @role_permission("Profesor")
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        plan_form = PlanCreateForm(request.POST)

        if plan_form.is_valid(): 
            plan_form.save(user)
            return  HttpResponseRedirect(reverse(self.success_url))
        else:
            context = self.get_context(form1=plan_form,)
            return render(request,self.template_name,context=context)

class PlanTrabajoDeleteView(AuthDeleteView):
    model = PlanTrabajo
    template_name = "plan_trabajo/profesor_delete_plan.html"
    success_url = 'estudiantes:profesor'
    
    def get_success_url(self):
        return reverse(self.success_url)
    
    def is_authorized(self, request,*args, **kwargs):
        obj = self.model.objects.get(id = self.kwargs['pk'])
        return request.user.id == obj.tutor_id

class PlanTrabajoUpdateView(AuthUpdateView):
    model = PlanTrabajo
    fields = ['estudiante', 'asignatura','curso','semestre','evaluacion']
    template_name = "plan_trabajo/profesor_edit_plan.html"
    success_url = 'estudiantes:profesor'

    def get_success_url(self):
        return reverse(self.success_url)

    def is_authorized(self, request,*args, **kwargs):
        obj = self.model.objects.get(id = self.kwargs['pk'])
        return request.user.id == obj.tutor_id

class EPlanTrabajoListView(ListView):
    model = PlanTrabajo
    template_name = "estudiante/estudiante_plan_list.html"
        
    def get_queryset(self):
        return PlanTrabajo.objects.filter(estudiante_id= self.kwargs['pk'])


class AdministrativeQueryView(FilterView):
    model = Estudiante
    fields = '__all__'
    template_name = "consultas/trabajador.html"

    @role_permission('Trabajador')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @role_permission('Trabajador')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class EstudianteQueryView(FilterView):
    model = Estudiante
    template_name = "consultas/estudiante.html"
    
    @role_permission('Estudiante')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @role_permission('Estudiante')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProfesorQueryView(FilterView):
    model = PlanTrabajo
    template_name = "consultas/profesor.html"

    @role_permission('Profesor')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @role_permission('Profesor')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
