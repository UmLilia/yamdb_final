from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .validators import valid_username

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""

    email = serializers.EmailField(
        max_length=254, required=True
    )
    username = serializers.CharField(
        max_length=150
    )

    def validate_email(self, value):
        """Проверка email на валидность."""
        try:
            validate_email(value)
        except ValidationError as error:
            raise ValidationError(
                f'Email не валидно: {error}'
            )
        return value

    def validate_username(self, value):
        """Проверка на me и на валидное username."""
        try:
            valid_username(value)
        except ValidationError as error:
            raise ValidationError(
                f'username не валидно: {error}'
            )
        return value

    def validate(self, data):
        if (
            User.objects.filter(username=data.get('username')).first()
            != User.objects.filter(email=data.get('email')).first()
        ):
            raise ValidationError(
                'Полученный email или username уже используется другим '
                'пользователем.'
            )
        return data

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализация выдачи пользователю токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
