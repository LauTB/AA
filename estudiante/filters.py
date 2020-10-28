import django_filters as df 
from estudiante.models import *


class AdministrativeFilter(df.FilterSet):
    class Meta:
        model = Estudiante
        fields = {
            'user__first_name':['icontains'], 
            'user__last_name':['icontains'],
            'etapa':['exact'], 
            'anno':['iexact'], 
            'carrera':['exact'],
        }

class EstudianteFilter(df.FilterSet):
    class Meta:
        model = Estudiante
        fields = {
            'user__first_name':['icontains'], 
            'user__last_name':['icontains'],
            'etapa':['exact'], 
            'anno': ['iexact'],
            'carrera':['exact'],
            'compatible':['icontains'], 
        }

class ProfesorFilter(df.FilterSet):
    class Meta:
        model = PlanTrabajo
        fields = {
            'estudiante__user__first_name':['icontains'], 
            'estudiante__user__last_name':['icontains'],
            'estudiante__etapa':['exact'], 
            'estudiante__anno':['iexact'], 
            'estudiante__carrera':['exact'], 
            'estudiante__compatible':['icontains'],
            'evaluacion':['exact'],
            'tutor__user__first_name':['icontains'],
            'tutor__user__last_name':['icontains'],
            'asignatura':['exact'],
        }
