# Generated by Django 3.2.6 on 2021-10-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0007_alter_venta_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='hora',
            field=models.TimeField(default='16:46:51'),
        ),
    ]
