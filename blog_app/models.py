from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blogpost(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    slug = models.CharField(max_length=100, verbose_name='Человекопонятный URL')
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Превью (изображение)')
    created_at = models.DateTimeField(verbose_name="Дата создания", default=timezone.now)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать?')
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
