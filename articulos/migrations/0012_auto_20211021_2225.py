# Generated by Django 3.2.6 on 2021-10-21 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0011_auto_20211021_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='costo',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='precio_especial',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='precio_mayorista',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='precio_unitario',
            field=models.IntegerField(),
        ),
    ]
