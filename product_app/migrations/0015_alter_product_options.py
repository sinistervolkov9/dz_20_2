# Generated by Django 4.2.2 on 2024-05-11 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0014_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_edit_publish', 'Can edit publish'), ('can_edit_description', 'Can edit description'), ('can_edit_category', 'Can edit category')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
