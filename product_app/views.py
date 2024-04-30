from django.urls import reverse_lazy
from django.utils.text import slugify
from .forms import ProductForm, VersionForm
from .models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory


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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    # fields = ('name', 'price', 'description', 'photo')
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
    form_class = ProductForm
    template_name = 'products/product_form.html'
    pk_url_kwarg = 'product_id'
    # fields = ('name', 'price', 'description', 'photo')


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)

        return context_data

        # products = context_data['object_list']
        #
        # for product in products:
        #     active_version = Version.objects.filter(product=product, is_current_version=True).first()
        #     product.active_version = active_version
        #
        # return context_data

    def get_success_url(self):
        # print(self.object)
        return reverse_lazy('products:product_detail', kwargs={'product_id': self.kwargs['product_id']})

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        formset.is_valid()

        if formset.is_valid():  # and form.is_valid():
            formset.instance = self.object
            formset.save()
        # else:
        #     return self.render_to_response(self.get_context_data(form=form, formset=formset))

        return super().form_valid(form)

class ProductDeleteView(DeleteView):
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
