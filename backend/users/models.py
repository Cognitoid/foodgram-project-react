from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import RegexUsernameValidator


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        null=False
    )
    username = models.CharField(
        verbose_name='Ник (юзернейм)',
        max_length=150,
        unique=True,
        validators=(RegexUsernameValidator,)
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        null=False
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь: {self.email}'
