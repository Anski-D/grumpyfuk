from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', views.PostListByCategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.PostListByTagView.as_view(), name='tag'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post'),
    path('author/<slug:slug>/', views.PostListByAuthorView.as_view(), name='author'),
]
