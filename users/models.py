# django
from django.db import models
from django.contrib.auth.models import AbstractUser
# modelo de configuracion
from configuracion.models import Configuracion


class User(AbstractUser):
    """Modelo de usuario.
    Se extiende de la clase base AbstractUser y se agrega campos.
    """
    rol_usuario = models.CharField(null=True, max_length=50)
    configuracion = models.ForeignKey(Configuracion, null=True, blank=True, on_delete=models.SET_NULL)

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A users with that email already exists.'
        }
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        """Return username."""
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """Return username."""
        return self.username
