from django.contrib import admin
from .models import Blogpost


@admin.register(Blogpost)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'content', 'preview', 'is_published', 'views')
