from django.views.generic import ListView, UpdateView , TemplateView,CreateView, DeleteView
from django.shortcuts import render
import django.forms as forms

class BackURLForm(forms.Form):
    success_url = forms.CharField(widget=forms.HiddenInput(),required=False)
    

def is_authorized_decorator(func):
    """
    Auxiliar decorator that verifies if the user is authorized, redirecting to an error template 
    in case of failure.  
    """
    def inner_func(self:AuthMixin,request,*args, **kwargs):
        if self.is_authorized(request,*args, **kwargs):
            return func(self, request, *args, **kwargs)
        else:
            context = self.get_error_context(request, *args, **kwargs)
            return render(request, self.error_template, context)
    return inner_func

class AuthMixin:
    error_template = 'error.html'
    
    def is_authorized(self, request,*args, **kwargs):
        return True
    
    def get_error_context(self, request, *args, **kwargs):
        return {'error':"No estas autorizado para acceder a esta página"}

def go_back_set_context_url_decorator(func):
    def inner_function(self,*args,**kwargs):
        context = func(self, *args, **kwargs)
        self.set_back_url_into_form(context)
        return context
    return inner_function

def go_back_set_success_url_decorator(func):
    def inner_function(self, *args, **kwargs):
        if hasattr(self, 'get_form'):
            form = self.get_form()
            back_url = self.get_back_url_from_form(form)
        else:
            back_url = self.get_back_url_from_meta()
        if back_url:
            self.success_url = back_url
        return func(self, *args, **kwargs)
    return inner_function

class GoBackMixin():
    back_form_name = 'form'
    back_url_field = 'success_url'
    
    def set_back_url_into_form(self, context):
        try:
            back_url = self.get_back_url_from_meta()
            if back_url:
                context[self.back_form_name].fields[self.back_url_field].initial = back_url
                context[f'{self.back_form_name}_literal'] = f'<input type="hidden" name="{self.back_url_field}" id="id_{self.back_url_field}" value="{back_url}">'
        except:
            pass
                
    def get_back_url_from_form(self, form):
        form.is_valid()
        return form.cleaned_data.get('success_url')
        
    def get_back_url_from_meta(self):
        return self.request.META.get('HTTP_REFERER')

class AuthListView(ListView, AuthMixin):
    
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(ListView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    def post(self, request, *args, **kwargs):
        return super(ListView,self).post(request, *args, **kwargs)

class AuthCreateView(CreateView, AuthMixin, GoBackMixin):
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(CreateView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    @go_back_set_success_url_decorator
    def post(self, request, *args, **kwargs):
        return super(CreateView,self).post(request, *args, **kwargs)

    @go_back_set_context_url_decorator
    def get_context_data(self, **kwargs):
        return super(CreateView, self).get_context_data(**kwargs)

class AuthDeleteView(DeleteView, AuthMixin, GoBackMixin):
    
    def get_form(self):
        return BackURLForm(self.request.POST)
    
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(DeleteView,self).get(request, *args, **kwargs)
    
    @go_back_set_context_url_decorator
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context[self.back_form_name] = self.get_form()
        return context
    
    @is_authorized_decorator
    @go_back_set_success_url_decorator
    def post(self, request, *args, **kwargs):
        return super(DeleteView,self).post(request, *args, **kwargs)
    
class AuthUpdateView(UpdateView, AuthMixin, GoBackMixin):
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(UpdateView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    @go_back_set_success_url_decorator
    def post(self, request, *args, **kwargs):
        return super(UpdateView,self).post(request, *args, **kwargs)
    
    @go_back_set_context_url_decorator
    def get_context_data(self, **kwargs):
        return super(UpdateView,self).get_context_data(**kwargs)
