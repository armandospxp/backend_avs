# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modelo de usuario.
    Se extiende de la clase base AbstractUser y se agrega campos.
    """

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
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username