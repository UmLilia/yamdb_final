from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import valid_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )

    confirmation_code = models.CharField(max_length=100, blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        validators=(valid_username,)
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Введите адрес эл.почты',
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name='О пользователе',
        help_text='Расскажите о себе',
        blank=True,
        null=True,
    )

    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        choices=USER_ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_superuser

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
