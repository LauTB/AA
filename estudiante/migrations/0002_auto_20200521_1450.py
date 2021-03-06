# Generated by Django 2.2.7 on 2020-05-21 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import estudiante.models


class Migration(migrations.Migration):

    dependencies = [
        ('asignatura', '0001_initial'),
        ('estudiante', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('inicio', models.DateField(verbose_name='Fecha de inicio de la ayudantía')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignatura.Carrera', verbose_name='Carrera')),
                ('compatible', models.ManyToManyField(to='asignatura.Asignatura', verbose_name='Asignaturas Compatibles')),
            ],
        ),
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etapa', models.IntegerField(unique=True, verbose_name='Etapa')),
                ('pago', models.FloatField(validators=[estudiante.models.positive], verbose_name='Pago')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('departamento', models.CharField(max_length=400, verbose_name='Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='PlanTrabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluacion', models.IntegerField(verbose_name='Evaluación')),
                ('curso', models.DateField(verbose_name='Curso')),
                ('semestre', models.SmallIntegerField(verbose_name='Semestre')),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignatura.Asignatura', verbose_name='Asignatura')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiante.Estudiante', verbose_name='Estudiante')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiante.Profesor', verbose_name='Redactado por')),
            ],
        ),
        migrations.CreateModel(
            name='Imparte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignatura.Asignatura', verbose_name='Asignatura')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignatura.Carrera', verbose_name='Carrera')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiante.Estudiante', verbose_name='Estudiante')),
            ],
        ),
        migrations.AddField(
            model_name='estudiante',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiante.Etapa', verbose_name='Etapa'),
        ),
    ]
