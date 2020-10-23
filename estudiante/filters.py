import django_filters as df 
from estudiante.models import *


class AdministrativeFilter(df.FilterSet):
    class Meta:
        model = Estudiante
        fields = ['user__first_name', 'user__last_name','etapa', 'anno', 'carrera' ]

class EstudianteFilter(df.FilterSet):
    class Meta:
        model = Estudiante
        fields = ['user__first_name', 'user__last_name','etapa', 'anno', 'carrera', 'compatible' ]

class ProfesorFilter(df.FilterSet):
    class Meta:
        model = PlanTrabajo
        fields = ['estudiante__user__first_name', 'estudiante__user__last_name',
                'estudiante__etapa', 'estudiante__anno', 'estudiante__carrera', 'estudiante__compatible',
                'evaluacion','tutor__user__first_name','tutor__user__last_name','asignatura' ]