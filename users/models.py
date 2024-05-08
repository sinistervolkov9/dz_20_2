from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Номер телефона')
    country = models.CharField(max_length=75, **NULLABLE, verbose_name='Страна')

    token = models.CharField(max_length=50, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
