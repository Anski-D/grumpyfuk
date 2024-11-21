from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Post, Category, Tag


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class PostListByCategoryView(generic.ListView):
    template_name = 'blog/list_view.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])

        return Post.objects.filter(categories=category).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subset_type'] = 'Category'
        context['subset_name'] = Category.objects.get(slug=self.kwargs['slug'])
        context['categories'] = Category.objects.all()

        return context


class PostListByTagView(generic.ListView):
    template_name = 'blog/list_view.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])

        return Post.objects.filter(tags=tag).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subset_type'] = 'Tag'
        context['subset_name'] = Tag.objects.get(slug=self.kwargs['slug'])
        context['categories'] = Category.objects.all()

        return context
