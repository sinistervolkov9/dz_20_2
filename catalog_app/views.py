from django.shortcuts import render, redirect
from .forms import CategoryForm


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:create_category')
    else:
        form = CategoryForm()
    return render(request, 'catalog/create_category.html', {'form': form})


# def some_view(request):
#     # Получение категории по ее идентификатору
#     category = Category.objects.get(id=1)
#     # Получение всех продуктов, связанных с этой категорией
#     products = category.products.all()
#     return render(request, 'template_name.html', {'products': products})
