from config.settings import CACHE_ENABLED
from django.core.cache import cache
from product_app.models import Product


def get_products_from_cache():
    if not CACHE_ENABLED:
        return Product.objects.filter(is_published=True)

    key = 'categories'
    products = cache.get(key)
    if products is not None:
        return products

    products = Product.objects.filter(is_published=True)
    cache.set(key, products, timeout=3600)

    return products
