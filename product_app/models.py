from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.CharField(max_length=250, **NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Фото')
    slug = models.CharField(max_length=100, verbose_name='Человекопонятный URL', unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать?')
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})
