"""User admin classes."""

# Django
from django.contrib import admin

# Models
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    admin.site.register(User)