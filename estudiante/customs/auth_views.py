from django.views.generic import ListView, UpdateView , TemplateView,CreateView, DeleteView
from django.shortcuts import render

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

class AuthListView(ListView, AuthMixin):
    
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(ListView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    def post(self, request, *args, **kwargs):
        return super(ListView,self).post(request, *args, **kwargs)

class AuthCreateView(CreateView, AuthMixin):
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(CreateView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    def post(self, request, *args, **kwargs):
        return super(CreateView,self).post(request, *args, **kwargs)

class AuthDeleteView(DeleteView, AuthMixin):
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(DeleteView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    def post(self, request, *args, **kwargs):
        return super(DeleteView,self).post(request, *args, **kwargs)

class AuthUpdateView(UpdateView, AuthMixin):
    @is_authorized_decorator
    def get(self, request, *args, **kwargs):
        return super(UpdateView,self).get(request, *args, **kwargs)
    
    @is_authorized_decorator
    def post(self, request, *args, **kwargs):
        return super(UpdateView,self).post(request, *args, **kwargs)
