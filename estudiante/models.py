from django.contrib.auth.models import AbstractUser
from django.db import models
from asignatura.models import Asignatura, Carrera, Pertenece

def positive(x):
    return x > 0

class Etapa(models.Model):    
    etapa = models.IntegerField("Etapa", unique=True)
    pago = models.FloatField("Pago", validators=(positive,))
    def __str__(self):
        return '{}'.format(self.etapa)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_administrative = models.BooleanField(default=False)

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    inicio = models.DateField("Fecha de inicio de la ayudantía", auto_now=False, auto_now_add=False)
    carrera = models.ForeignKey(Carrera, verbose_name="Carrera", on_delete=models.CASCADE )
    etapa =  models.ForeignKey(Etapa, verbose_name="Etapa", on_delete=models.CASCADE)
    compatible = models.ManyToManyField(Asignatura, verbose_name="Asignaturas Compatibles")

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    departamento = models.CharField("Departamento", max_length=400)

class PlanTrabajo(models.Model):
    plan_file_path = 'static/planes/'
    evaluacion = models.IntegerField("Evaluación")
    curso = models.DateField("Curso")
    semestre = models.SmallIntegerField("Semestre")
    asignatura = models.ForeignKey(Asignatura, verbose_name = "Asignatura", on_delete = models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, verbose_name="Estudiante", on_delete=models.CASCADE)
    tutor = models.ForeignKey(Profesor, verbose_name="Redactado por", on_delete=models.CASCADE)

class Imparte(models.Model):
    estudiante = models.ForeignKey(Estudiante, verbose_name = "Estudiante", on_delete = models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, verbose_name = "Asignatura", on_delete = models.CASCADE)
    carrera = models.ForeignKey(Carrera, verbose_name = "Carrera", on_delete = models.CASCADE)


