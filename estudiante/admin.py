from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from estudiante.models import User, Estudiante, Profesor, Imparte, PlanTrabajo, Etapa

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Imparte)
admin.site.register(PlanTrabajo)
admin.site.register(Etapa)