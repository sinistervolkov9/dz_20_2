from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'object_list'
    extra_context = {'title': 'Новинки'}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True).order_by('-id')[:3]


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'object_list'
    # queryset = Product.objects.all()
    extra_context = {'title': 'Все товары'}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    extra_context = {'title': 'Товар'}

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ('name', 'price', 'description', 'photo', 'is_published')
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        if form.is_valid():
            product = form.save(commit=False)
            product.slug = slugify(product.name)
            product.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    pk_url_kwarg = 'product_id'
    fields = ('name', 'price', 'description', 'photo', 'is_published')

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'product_id': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_is_delete.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('products:product_list')
