"""Usuarios serializers."""

# Django
from django.contrib.auth import password_validation, authenticate

# Django REST Framework
from django.core.validators import FileExtensionValidator, RegexValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from rest_framework.validators import UniqueValidator
from usuarios.models import Usuario


class UsuarioModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'Usuarioname',
            'first_name',
            'last_name',
            'email',
        )


class UsuarioLoginSerializer(serializers.Serializer):
    # Campos que vamos a requerir
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    # Primero validamos los datos
    def validate(self, data):
        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        Usuario = authenticate(Usuarioname=data['email'], password=data['password'])
        if not Usuario:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['Usuario'] = Usuario
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(Usuario=self.context['Usuario'])
        return self.context['Usuario'], token.key


class UsuarioSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Usuario.objects.all())]
    )
    Usuarioname = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=Usuario.objects.all())]
    )

    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=False
    )

    extract = serializers.CharField(max_length=1000, required=False)

    city = serializers.CharField(max_length=250, required=False)

    country = serializers.CharField(max_length=250, required=False)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Debes introducir un número con el siguiente formato: +999999999. El límite son de 15 dígitos."
    )
    phone = serializers.CharField(validators=[phone_regex], required=False)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=100)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)

        image = None
        if 'photo' in data:
            image = data['photo']

        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(
                    f"La imagen es demasiado grande, el peso máximo permitido es de 512KB y el tamaño enviado es de {round(image.size / 1024)}KB")

        return data

    def create(self, data):
        data.pop('password_confirmation')
        usuario = Usuario.objects.create_Usuario(**data)
        return usuario
