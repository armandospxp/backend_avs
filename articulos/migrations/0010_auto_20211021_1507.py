# Generated by Django 3.2.6 on 2021-10-21 18:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0009_alter_articulo_unidad_medida'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='estado',
            field=models.CharField(choices=[('A', 'Activo'), ('H', 'Historico')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='articulo',
            name='fecha_creacion',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='marca',
            name='estado',
            field=models.CharField(choices=[('A', 'Activo'), ('H', 'Historico')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='marca',
            name='fecha_creacion',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
