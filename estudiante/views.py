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
from estudiante.customs.auth_views import AuthListView, AuthDeleteView, AuthUpdateView, AuthCreateView, is_authorized_decorator, go_back_set_success_url_decorator


from excel_response import ExcelView

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

class IndexView(TemplateView):
    template_name = "estudiante/index.html"

class EtapaListView(ListView):
    model = Etapa
    template_name = "consultas/etapa.html"

class EtapaExcelView(ExcelView):
    model = Etapa
    template_name = "consultas/etapa.html"

    output_filename=f'{model.__name__}_data'
    worksheet_name=f'{model.__name__}'
    force_csv=False
    header_font=None
    data_font=None
    guess_types=True
           


class EstudianteUpdateView(AuthUpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "estudiante/estudiante_edit.html"
    success_url = 'estudiantes:index'
    object=None
    next = 'estudiante/user_estudiante'

    def get_success_url(self):
        try:
            return reverse(self.success_url)
        except:
            return self.success_url
    
    @role_permission('Estudiante')
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        student = kwargs.pop('estudiante','')
        user_object = request.user
        user = User.objects.filter(id = user_object.id).get()
        user_form = UserUpdateForm(instance=user)
        student = Estudiante.objects.get(user_id= request.user.id)
        student_form = EstudianteUpdateForm(instance=student)
        context = self.get_context_data(form=user_form, form1=student_form)
        return render(request,self.template_name,context=context)

    @role_permission('Estudiante')
    @is_authorized_decorator
    @go_back_set_success_url_decorator
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        student = Estudiante.objects.get(user_id= request.user.id)
        user_form = UserUpdateForm(request.POST, instance=user)
        student_form = EstudianteUpdateForm(request.POST, instance=student)
        student_form.instance.Estudiante = student
        
        if user_form.is_valid() and student_form.is_valid():
            user_form.save(user)
            student=student_form.save(user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data(form=user_form, form1=student_form)
            return render(request,self.template_name,context=context)

class ProfesorUpdateView(AuthUpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "estudiante/profesor_edit.html"
    success_url = 'estudiantes:index'
    object = None
    next = 'estudiante/user_profesor'

    def get_success_url(self):
        try:
            return reverse(self.success_url)
        except:
            return self.success_url

    @role_permission('Profesor')
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        profesor = kwargs.pop('profesor','')
        user_object = request.user
        user = User.objects.filter(username= user_object).get()
        user_form = UserUpdateForm(instance=user)
        profesor = Profesor.objects.get(user_id= request.user.id)
        profesor_form = ProfesorUpdateForm(instance=profesor)
        context = self.get_context_data(form=user_form,form1=profesor_form)
        return render(request,self.template_name,context=context)

    @role_permission('Profesor')
    @is_authorized_decorator
    @go_back_set_success_url_decorator
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        profesor = Profesor.objects.get(user_id= request.user.id)
        user_form = UserUpdateForm(request.POST, instance=user)
        profesor_form = ProfesorUpdateForm(request.POST, instance=profesor)
        profesor_form.instance.Profesor = profesor
        
        if user_form.is_valid() and profesor_form.is_valid():
            user = user_form.save()
            profesor = profesor_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data(form=user_form, form1=profesor_form)
            return render(request,self.template_name,context=context)

class AdministrativeUpdateView(AuthUpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "estudiante/administrative_edit.html"
    success_url = 'estudiantes:index'
    next = 'estudiante/user_profesor'

    def get_success_url(self):
        try:
            return reverse(self.success_url)
        except:
            return self.success_url

    @role_permission('Trabajador')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @role_permission('Trabajador')
    def post(self, request, *args, **kwargs):
        return super().post(request,*args,**kwargs)
    
class PasswordChangeView( PasswordChangeView):
    template_name = "estudiante/password_change.html"
    success_url = reverse_lazy('login')


class PlanTrabajoListView(ListView):
    model = PlanTrabajo
    template_name = "plan_trabajo/profesor_plan_trabajo.html"

    def get_queryset(self):
        return PlanTrabajo.objects.filter(tutor_id= self.kwargs['pk'])

class PlanTrabajoCreateView(AuthCreateView):
    model = PlanTrabajo
    form_class = PlanCreateForm
    template_name = "plan_trabajo/profesor_add_plan.html"
    success_url = 'estudiantes:index'

    def get_success_url(self):
        try: 
            return reverse(self.success_url)
        except:
            return self.success_url   

    @role_permission("Profesor")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @role_permission("Profesor")
    @is_authorized_decorator
    @go_back_set_success_url_decorator
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id= request.user.id)
        plan_form = PlanCreateForm(request.POST)

        if plan_form.is_valid(): 
            plan_form.save(user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context(form=plan_form,)
            return render(request,self.template_name,context=context)

class PlanTrabajoDeleteView(AuthDeleteView):
    model = PlanTrabajo
    template_name = "plan_trabajo/profesor_delete_plan.html"
    success_url = 'estudiantes:index'
    
    def get_success_url(self):
        try: 
            return reverse(self.success_url)
        except:
            return super().get_success_url()    
    
    def is_authorized(self, request,*args, **kwargs):
        obj = self.model.objects.get(id = self.kwargs['pk'])
        return request.user.id == obj.tutor_id

class PlanTrabajoUpdateView(AuthUpdateView):
    model = PlanTrabajo
    form_class = PlanUpdateForm
    template_name = "plan_trabajo/profesor_edit_plan.html"
    success_url = 'estudiantes:index'

    def get_success_url(self):
        try: 
            return reverse(self.success_url)
        except:
            return super().get_success_url()
        
    def is_authorized(self, request,*args, **kwargs):
        obj = self.model.objects.get(id = self.kwargs['pk'])
        return request.user.id == obj.tutor_id

class EPlanTrabajoListView(ListView):
    model = PlanTrabajo
    template_name = "estudiante/estudiante_plan_list.html"
        
    def get_queryset(self):
        return PlanTrabajo.objects.filter(estudiante_id= self.kwargs['pk'])


class EPlanTrabajoExcelView(ExcelView):
    model = PlanTrabajo
    template_name = "estudiante/estudiante_plan_list.html"

    output_filename = f'{model.__name__}_data'
    worksheet_name = f'{model.__name__}'
    force_csv = False
    header_font = None
    data_font = None
    guess_types = True


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


class EstudianteQueryExcelView(ExcelView):
    model = Estudiante
    template_name = "consultas/estudiante.html"

    output_filename = f'{model.__name__}_data'
    worksheet_name = f'{model.__name__}'
    force_csv = False
    header_font = None
    data_font = None
    guess_types = True

class ProfesorQueryView(FilterView):
    model = PlanTrabajo
    template_name = "consultas/plan_de_trabajo.html"

    @role_permission('Profesor')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @role_permission('Profesor')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfesorQueryExcelView(FilterView):
    model = PlanTrabajo
    template_name = "consultas/plan_de_trabajo.html"
    
    output_filename = f'{model.__name__}_data'
    worksheet_name = f'{model.__name__}'
    force_csv = False
    header_font = None
    data_font = None
    guess_types = True
