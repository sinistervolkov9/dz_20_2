# Generated by Django 4.2.2 on 2024-05-11 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog_app', '0001_initial'),
        ('product_app', '0009_version_only_one_active_version_for_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog_app.Category'),
        ),
    ]