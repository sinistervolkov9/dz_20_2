from django.db import models
from django.db.models import Q
from catalog_app.models import Category
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    # ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, default=1, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.CharField(max_length=250, **NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Фото')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать?')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

        permissions = [
            ("can_edit_publish", "Can edit publish"),
            ("can_edit_description", "Can edit description"),
            ("can_edit_category", "Can edit category"),
                       ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.CharField(max_length=50, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current_version = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f"{self.product.name} - {self.version_number}"

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=Q(is_current_version=True),
                name='only_one_active_version_for_product',
            ),
        ]
