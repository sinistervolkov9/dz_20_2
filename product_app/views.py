from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
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
