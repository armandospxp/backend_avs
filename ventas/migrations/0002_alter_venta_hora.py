# Generated by Django 3.2.6 on 2021-10-14 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='hora',
            field=models.TimeField(default='22:46:19'),
        ),
    ]
