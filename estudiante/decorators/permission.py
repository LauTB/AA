from django.shortcuts import render

# Decorator template
def param_decorator(param0,param1,param2): # Params Function
    def wrap_func(func): # Wrap Function
       def inner_func(*args,**kwargs): # Inner Function
            # Something to do before the func call
            value = func(*args,**kwargs)
            # Something to do after the func call
            return value
       return inner_func
    return wrap_func

def role_permission(role:str, method_wrapper=True,error_template:str='error.html'):
    """
    role: the user from the request must have be a `role` user.
    method_wrapper: If the decorator is wrapping a class method.     
    Verify if the user is of type `role` redirecting to `error_template` in case of failure
    """
    def wrap_func(func):
        def inner_func(request, *args, **kwargs):
            self = request
            if method_wrapper:
                # the first arg in a method is the self instance
                request = args[0]
            ok = False
            if role == 'Profesor':
                ok = request.user.is_teacher
            if role == 'Estudiante':
                ok = request.user.is_student
            if role == 'Trabajador':
                ok = request.user.is_administrative
            if ok:
                return func(self, *args, **kwargs)
            else:
                return render(request, error_template, {'error':f'Tienes que ser {role} para poder acceder a esta página'})
        return inner_func
    return wrap_func