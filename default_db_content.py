from estudiante.models import *
from asignatura.models import *


# Run in django shell by:
#    >> python3 manage.py shell
#    >> import app.default_de_content

# stage1 = Etapa(etapa= 1, pago= 25)
# #stage1.save()
# stage = Etapa(etapa= 2, pago= 35)
# stage.save()
# stage = Etapa(etapa= 3, pago= 45)
# stage.save()
# stage = Etapa(etapa= 4, pago= 55)
# stage.save()



subject = Asignatura(nombre = "Álgebra I")
#subject.save()
subject = Asignatura(nombre = "Compilación I")
#subject.save()
subject = Asignatura(nombre = "Geometría Analítica")
#subject.save()

career = Carrera(nombre = "Matemática")
#career.save()
career = Carrera.objects.get(nombre = 'Matemática')
career.asignaturas.add(*[Asignatura.objects.get(nombre='Geometría Analítica')])
career = Carrera(nombre = "Ciencias de la Computación")
career.save()
career.asignaturas.add(*[Asignatura.objects.get(nombre='Geometría Analítica')])

