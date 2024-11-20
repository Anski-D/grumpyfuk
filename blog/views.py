from django.shortcuts import render
from django.views import generic

from .models import Post, Category, Tag


def index(request):
    context = {
        'posts': Post.objects.all().order_by('-created'),
        'categories': Category.objects.all(),
    }

    return render(request, 'blog/index.html', context)


def blog_category(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'category': category,
        'categories': Category.objects.all(),
        'posts': Post.objects.filter(categories=category).order_by('-created'),
    }

    return render(request, 'blog/category.html', context)


def blog_tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    context = {
        'tag': tag,
        'categories': Category.objects.all(),
        'posts': Post.objects.filter(tags=tag).order_by('-created'),
    }

    return render(request, 'blog/tag.html', context)
