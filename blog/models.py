from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    tags = models.ManyToManyField('Tag', related_name='posts')
    author = models.ForeignKey('Author', related_name='posts', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=36, unique=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})


class Author(models.Model):
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    display_name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=36, unique=True)

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('blog:author-post-list', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=36, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category-post-list', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=36, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag-post-list', kwargs={'slug': self.slug})


class Comment(models.Model):
    author = models.CharField(max_length=36)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=36, unique=True)

    def __str__(self):
        return f'{self.author} on {self.post}'
