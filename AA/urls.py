"""AA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, PasswordResetView, logout_then_login
from AA import views
from AA.views import Login, RegisterView, StudentRegistrationView, TeacherRegistrationView, AdministrativeRegistrationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('registrar/', RegisterView.as_view(), name='register'),
    path('logout/', logout_then_login, name='logout'),
    path('', include(('estudiante.urls', 'estudiantes'), namespace="estudiantes")),
    path('asignatura/', include('asignatura.urls')),
    path('registrar_est/', StudentRegistrationView.as_view(), name='est'),
    path('registrar_prof/', TeacherRegistrationView.as_view(), name='prof'),
    path('registrar_trab/',  AdministrativeRegistrationView.as_view(), name='trab'),
]
