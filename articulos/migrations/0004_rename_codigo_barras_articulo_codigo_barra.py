# Generated by Django 3.2.6 on 2021-10-21 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0003_articulo_codigo_barras'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articulo',
            old_name='codigo_barras',
            new_name='codigo_barra',
        ),
    ]
