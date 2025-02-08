from abc import ABC

from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import Post, Category, Tag, Author, Image


def _get_sorted_published_posts():
    return Post.objects.filter(published=True).filter(publish_date__lte=timezone.now()).order_by('-publish_date')


def _get_published_categories():
    return Category.objects.filter(posts__published=True).filter(posts__publish_date__lte=timezone.now()).distinct()


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return _get_sorted_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = _get_published_categories()
        context['absolute_uri'] = self.request.build_absolute_uri()

        return context


class PostListBySubsetView(ABC, IndexView):
    template_name = 'blog/post_list.html'

    @property
    def model_name(self):
        return self.model._meta.object_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model_name
        context['object'] = self.model.objects.get(slug=self.kwargs["slug"])

        return context

    def _get_subset(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class PostListByCategoryView(PostListBySubsetView):
    model = Category

    def get_queryset(self):
        return super().get_queryset().filter(categories=self._get_subset())


class PostListByTagView(PostListBySubsetView):
    model = Tag

    def get_queryset(self):
        return super().get_queryset().filter(tags=self._get_subset())


class PostDetailView(generic.DetailView):
    model = Post

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()

        return _get_sorted_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = _get_published_categories()
        post = self.model.objects.get(slug=self.kwargs['slug'])
        if post.last_updated.date() > post.publish_date.date():
            context['last_updated'] = post.last_updated

        context['absolute_uri'] = self.request.build_absolute_uri(post.get_absolute_url())

        return context


class ImageFileRedirectView(generic.RedirectView):
    model = Image
    permanent = True
    pattern_name = 'image-file'

    def get_redirect_url(self, *args, **kwargs):
        image = get_object_or_404(self.model, slug=kwargs['slug'])

        return image.image.url


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = _get_published_categories()
        context['published_posts'] = _get_sorted_published_posts().filter(author=self.object)

        return context
