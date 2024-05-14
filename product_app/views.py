from django.urls import reverse_lazy
from django.utils.text import slugify
from .forms import ProductForm, VersionForm, ProductManagerForm
from .models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from product_app.services import get_products_from_cache


class IndexView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'object_list'
    extra_context = {'title': 'Новинки'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = context['object_list']

        for product in products:
            active_version = Version.objects.filter(product=product, is_current_version=True).first()
            product.active_version = active_version

        context['object_list'] = products

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset.order_by('-id')[:3]


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'object_list'
    # queryset = Product.objects.all()
    extra_context = {'title': 'Все товары'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = context['object_list']

        for product in products:
            active_version = Version.objects.filter(product=product, is_current_version=True).first()
            product.active_version = active_version

        context['object_list'] = products

        return context

    def get_queryset(self):
        return get_products_from_cache()
        # return Product.objects.all()

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    extra_context = {'title': 'Товар'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        active_version = Version.objects.filter(product=product, is_current_version=True).first()

        context['active_version'] = active_version

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    # fields = ('name', 'price', 'category', 'description', 'is_published')
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.name)

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        # return reverse_lazy('products:product_detail', kwargs={'product_id': self.kwargs['product_id']})
        return reverse_lazy('products:product_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (user.has_perm("product_app.can_edit_publish") and user.has_perm("product_app.can_edit_description")
                and user.has_perm("product_app.can_edit_category")):
            return ProductManagerForm
        raise PermissionDenied

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_is_delete.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('products:product_list')

# ----------------------------------------------------------------------------------------------------------------------

class VersionListView(ListView):
    model = Version

    def get_queryset(self, *args, **kwargs):
        queryset = Version.objects.all()
        products = Product.objects.all()
        for product in products:
            print(product)
            versions = Version.objects.filter(product=product)
            print(queryset.product == product)
            return versions
        return Version.objects.filter(product=Product.objects.get(pk=self.kwargs.get('pk')))


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('products:products')


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('products:products')


class VersionDetailView(DetailView):
    model = Version
    context_object_name = 'versions'


class VersionDeleteView(DeleteView):
    model = Version
    success_url = reverse_lazy('products:versions')
