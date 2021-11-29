# Generated by Django 3.2.6 on 2021-11-29 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0003_rename_numero_facrura_configuracion_numero_factura'),
        ('users', '0002_user_rol_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='configuracion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='configuracion.configuracion'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rol_usuario',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
