import django_filters as df 
from estudiante.models import *


class AdministrativeFilter(df.FilterSet):
    anno = df.ChoiceFilter('anno',lookup_expr='iexact',label='Año',choices=valid_year_choices)
    class Meta:
        model = Estudiante
        fields = {
            'user__first_name':['icontains'], 
            'user__last_name':['icontains'],
            'etapa':['exact'], 
            'carrera':['exact'],
        }

class EstudianteFilter(df.FilterSet):
    anno = df.ChoiceFilter('anno',lookup_expr='iexact',label='Año',choices=valid_year_choices)
    class Meta:
        model = Estudiante
        fields = {
            'user__first_name':['icontains'], 
            'user__last_name':['icontains'],
            'etapa':['exact'], 
            'carrera':['exact'],
            'compatible':['icontains'], 
        }

class ProfesorFilter(df.FilterSet):
    anno = df.ChoiceFilter('estudiante__anno',lookup_expr='iexact',label='Año',choices=valid_year_choices)
    anno = df.ChoiceFilter('evaluacion',lookup_expr='exact',label='Evaluación',choices=valid_evaluation_choices)
    class Meta:
        model = PlanTrabajo
        fields = {
            'estudiante__user__first_name':['icontains'], 
            'estudiante__user__last_name':['icontains'],
            'estudiante__etapa':['exact'], 
            'estudiante__carrera':['exact'], 
            'estudiante__compatible':['icontains'],
            'tutor__user__first_name':['icontains'],
            'tutor__user__last_name':['icontains'],
            'asignatura':['exact'],
        }
