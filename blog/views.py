from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Post, Category, Tag, Author


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
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])

        return Post.objects.filter(categories=category).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = f'Category: {Category.objects.get(slug=self.kwargs["slug"])}'
        context['categories'] = Category.objects.all()

        return context


class PostListByTagView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])

        return Post.objects.filter(tags=tag).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = f'Tag: {Tag.objects.get(slug=self.kwargs["slug"])}'
        context['categories'] = Category.objects.all()

        return context


class PostListByAuthorView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        author = get_object_or_404(Author, slug=self.kwargs['slug'])

        return Post.objects.filter(author=author).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = f'Author: {Author.objects.get(slug=self.kwargs["slug"])}'
        context['categories'] = Category.objects.all()

        return context


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context
