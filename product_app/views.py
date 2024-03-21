from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product


def base(request):
    # product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/base.html') # {'product': product})
