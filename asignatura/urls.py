from django.urls import path, include
from asignatura.views import index

urlpatterns = [
    path('asignaturas/', index),
]