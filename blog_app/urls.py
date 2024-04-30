from django.urls import path
from .apps import BlogAppConfig
from .views import BlogpostListView, BlogpostCreateView, BlogpostUpdateView, BlogpostDeleteView, BlogpostDetailView

app_name = BlogAppConfig.name

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('blog_list/', BlogpostListView.as_view(), name='blog_list'),
    path('blogs/<int:blog_id>/', BlogpostDetailView.as_view(), name='blog_detail'),
    path('blogs/create', BlogpostCreateView.as_view(), name='blog_create'),
    path('blogs/<int:blog_id>/update', BlogpostUpdateView.as_view(), name='blog_update'),
    path('blogs/<int:blog_id>/delete', BlogpostDeleteView.as_view(), name='blog_delete'),
]
