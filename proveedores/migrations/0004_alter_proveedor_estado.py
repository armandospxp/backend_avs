# Generated by Django 3.2.6 on 2021-10-21 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0003_auto_20211021_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='estado',
            field=models.CharField(choices=[('A', 'ACTIVO'), ('H', 'HISTORICO')], default='A', max_length=1),
        ),
    ]
