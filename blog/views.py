from abc import ABC
from urllib import request

from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone
from django.views.generic.base import RedirectView

from .models import Post, Category, Tag, Author, Image


def _get_sorted_published_posts():
    return Post.objects.filter(published=True).filter(publish_date__lte=timezone.now()).order_by('-publish_date')


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    categories = Category.objects.filter(posts__published=True).filter(posts__publish_date__lte=timezone.now()).distinct()

    def get_queryset(self):
        return _get_sorted_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        context['absolute_uri'] = self.request.build_absolute_uri()

        return context


class PostListBySubsetView(ABC, IndexView):
    template_name = 'blog/post_list.html'
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = f'{self.title}: {self.model.objects.get(slug=self.kwargs["slug"])}'

        return context

    def _get_subset(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class PostListByCategoryView(PostListBySubsetView):
    model = Category
    title = 'Category'

    def get_queryset(self):
        return super().get_queryset().filter(categories=self._get_subset())


class PostListByTagView(PostListBySubsetView):
    model = Tag
    title = 'Tag'

    def get_queryset(self):
        return super().get_queryset().filter(tags=self._get_subset())


class PostListByAuthorView(PostListBySubsetView):
    model = Author
    title = 'Author'

    def get_queryset(self):
        return super().get_queryset().filter(author=self._get_subset())


class PostDetailView(generic.DetailView):
    model = Post
    categories = Category.objects.filter(posts__published=True).filter(posts__publish_date__lte=timezone.now()).distinct()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()

        return _get_sorted_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        post = self.model.objects.get(slug=self.kwargs['slug'])
        if post.last_updated.date() > post.publish_date.date():
            context['last_updated'] = post.last_updated

        context['absolute_uri'] = self.request.build_absolute_uri(post.get_absolute_url())

        return context


class ImageFileRedirectView(RedirectView):
    model = Image
    permanent = True
    pattern_name = 'image-file'

    def get_redirect_url(self, *args, **kwargs):
        image = get_object_or_404(self.model, slug=kwargs['slug'])

        return image.image.url
