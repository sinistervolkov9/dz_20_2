from django.urls import path
from .apps import ProductAppConfig
from .views import IndexView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = ProductAppConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:product_id>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:product_id>/delete', ProductDeleteView.as_view(), name='product_delete'),
]
