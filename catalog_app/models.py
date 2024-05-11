from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    