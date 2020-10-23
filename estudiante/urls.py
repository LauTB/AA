from django.urls import path
from estudiante import views
from estudiante.views import (EstudianteUpdateView,ProfesorUpdateView, AdministrativeUpdateView,
                            PasswordChangeView, PlanTrabajoListView,PlanTrabajoCreateView,
                            EPlanTrabajoListView,AdministrativeQueryView,EstudianteQueryView,
                            ProfesorQueryView, PlanTrabajoDeleteView, PlanTrabajoUpdateView,)
from .filters import *

urlpatterns = [
    path('user_estudiante/', views.user_estudiante,name='estudiante'),
    path('user_profesor/', views.user_profesor,name='profesor'),
    path('user_trabajador/', views.user_administrative,name='trabajador'),
    path('editar_estudiante/<int:pk>', EstudianteUpdateView.as_view(), name= 'estudiante_edit'),
    path('editar_profesor/<int:pk>', ProfesorUpdateView.as_view(), name= 'profesor_edit'),
    path('editar_trabajador/<int:pk>', AdministrativeUpdateView.as_view(), name= 'trabajador_edit'),
    path('cambiar_password/', PasswordChangeView.as_view(), name= 'pass_change'),
    path('listar_planes/<int:pk>', PlanTrabajoListView.as_view(), name= 'plan_list'),
    path('nuevo_plan/', PlanTrabajoCreateView.as_view(), name= 'plan_create'),
    path('mis_planes/<int:pk>', EPlanTrabajoListView.as_view(), name= 'plan_est'),
    path('user_trabajador/consulta/', AdministrativeQueryView.as_view(filterset_class = AdministrativeFilter),name='trabajador_consulta'),
    path('user_profesor/consulta/', ProfesorQueryView.as_view(filterset_class = ProfesorFilter),name='profesor_consulta'),
    path('user_estudiante/consulta/', EstudianteQueryView.as_view(filterset_class = EstudianteFilter),name='estudiante_consulta'),
    path('<int:pk>/eliminar', PlanTrabajoDeleteView.as_view(), name= 'plan_eliminar'),
    path('<int:pk>/editar', PlanTrabajoUpdateView.as_view(), name= 'plan_editar'),

]
