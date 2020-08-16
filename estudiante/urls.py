from django.urls import path
from estudiante import views
from estudiante.views import EstudianteListView, StudentUpdateView, TeacherUpdateView, AdministrativeUpdateView

urlpatterns = [
    path('user_estudiante/', views.user_estudiante,name='estudiante'),
    path('user_profesor/', views.user_profesor,name='profesor'),
    path('listar_estudiantes/', EstudianteListView.as_view(), name= 'listado'),
    path('testing/<int:pk>/', TeacherUpdateView.as_view(), name= 'listado'),
]