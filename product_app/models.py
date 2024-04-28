from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    # ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.CharField(max_length=250, **NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Фото')

    def __str__(self):
        return f'{self.name}'
