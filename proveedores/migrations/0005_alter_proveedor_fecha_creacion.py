# Generated by Django 3.2.6 on 2021-11-02 23:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0004_alter_proveedor_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
