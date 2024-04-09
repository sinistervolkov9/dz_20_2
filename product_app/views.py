from django.shortcuts import render
from .models import Product

def index(request):
    context = {
        'object_list': Product.objects.all().order_by('-id')[:3],
        'title': 'Новинки'
    }
    return render(request, 'products/index.html', context)  # {'product': product})


def all_products(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Все товары'
    }
    return render(request, 'products/all_products.html', context)  # {'product': product})


def product_detail(request, product_id):
    context = {
        'object_list': Product.objects.all(),
        'title': Product.objects.get(pk=product_id),
    }
    return render(request, 'products/product_detail.html', context)
