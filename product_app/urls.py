from django.urls import path
from .views import base

urlpatterns = [
    # path('product/<int:pk>/', base, name='product_detail'),
    path('', base, name='base'),
    # path('', index, name='index'),
]
