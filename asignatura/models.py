from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asignatura(models.Model):
    nombre = models.CharField("Nombre", max_length=200, unique=True)
    class Meta(User.Meta):
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'
    def __str__(self):
        return '{}'.format(self.nombre)
    

class Carrera(models.Model):
    nombre = models.CharField("Nombre", max_length=200,unique=True)
    asignaturas = models.ManyToManyField(Asignatura, )
    class Meta(User.Meta):
        verbose_name = 'carrera'
        verbose_name_plural = 'carreras'
    #subjects_impart = models.ManyToManyField(Asignatura, through='app.Impart', through_fields=('career','subject'), verbose_name="Asignaturas impartidas")
    def __str__(self):
        return '{}'.format(self.nombre)
    

class Pertenece(models.Model):
    asignatura = models.ForeignKey(Asignatura, verbose_name= "Asignatura", on_delete=models.CASCADE)    
    carrera = models.ForeignKey(Carrera, verbose_name="Carrera", on_delete=models.CASCADE)
    anno = models.PositiveIntegerField("Año") 

    semestre = models.IntegerField("Semestre")
    class Meta:
        unique_together = ('carrera','asignatura','semestre')   
    

