from django.apps import AppConfig


class ArticulosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articulos'

class MarcaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marcas'
