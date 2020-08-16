from django.contrib import admin
from asignatura.models import Asignatura, Carrera, Pertenece

# Register your models here.
admin.site.register(Asignatura)
admin.site.register(Carrera)
admin.site.register(Pertenece)
