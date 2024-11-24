from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', views.PostListByCategoryView.as_view(), name='category-post-list'),
    path('tag/<slug:slug>/', views.PostListByTagView.as_view(), name='tag-post-list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('author/<slug:slug>/', views.PostListByAuthorView.as_view(), name='author-post-list'),
]
