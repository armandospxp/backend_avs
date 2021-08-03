# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """Modelo de usuario.
    Se extiende de la clase base AbstractUser y se agrega campos.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username