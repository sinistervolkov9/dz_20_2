from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Blogpost
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class BlogpostListView(ListView):
    model = Blogpost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'object_list'
    extra_context = {'title': 'Все блоги'}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class BlogpostDetailView(DetailView):
    model = Blogpost
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_id'
    extra_context = {'title': 'Блог'}

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


# class BlogpostCreateView(CreateView):
#     model = Blogpost
#     template_name = 'blogs/blog_form.html'
#     fields = ('title', 'content', 'preview', 'is_published')
#     success_url = reverse_lazy('blogs:blog_list')
#
#     def form_valid(self, form):
#         if form.is_valid():
#             blog = form.save(commit=False)
#             blog.slug = slugify(blog.title)
#             blog.save()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#
# class BlogpostUpdateView(UpdateView):
#     model = Blogpost
#     template_name = 'blogs/blog_form.html'
#     pk_url_kwarg = 'blog_id'
#     fields = ('title', 'content', 'preview', 'is_published')
#
#     def get_success_url(self):
#         return reverse_lazy('blogs:blog_detail', kwargs={'blog_id': self.object.pk})
#
#
# class BlogpostDeleteView(DeleteView):
#     model = Blogpost
#     template_name = 'blogs/blog_is_delete.html'
#     pk_url_kwarg = 'blog_id'
#     success_url = reverse_lazy('blogs:blog_list')

class BlogpostCreateView(LoginRequiredMixin, CreateView):
    model = Blogpost
    template_name = 'blogs/blog_form.html'
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blogs:blog_list')

    def form_valid(self, form):
        # Привязываем текущего пользователя к создаваемой записи блога
        form.instance.author = self.request.user
        # Генерируем slug из заголовка записи блога
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class BlogpostUpdateView(LoginRequiredMixin, UpdateView):
    model = Blogpost
    template_name = 'blogs/blog_form.html'
    pk_url_kwarg = 'blog_id'
    fields = ('title', 'content', 'preview', 'is_published')

    def get_success_url(self):
        return reverse_lazy('blogs:blog_detail', kwargs={'blog_id': self.object.pk})


class BlogpostDeleteView(LoginRequiredMixin, DeleteView):
    model = Blogpost
    template_name = 'blogs/blog_is_delete.html'
    pk_url_kwarg = 'blog_id'
    success_url = reverse_lazy('blogs:blog_list')