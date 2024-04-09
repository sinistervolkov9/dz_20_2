from django.urls import path
from .views import index, all_products, product_detail
from .apps import ProductAppConfig

app_name = ProductAppConfig.name

urlpatterns = [
    # path('product/<int:pk>/', base, name='product_detail'),
    path('', index, name='index'),  # index - это контроллер!!!
    path('all_products/', all_products, name='all_products'),  # all_products - это контроллер!!!
    path('products/<int:product_id>/', product_detail, name='product_detail'),
]
