from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

_SLUG_LENGTH = 64


def _image_save_name(instance, filename):
    suffix = Path(filename).suffix

    return f'images/{instance.slug}-{timezone.now().strftime("%Y%m%d%H%M%S")}{suffix}'


class Post(models.Model):
    _summary_length = 500

    title = models.CharField(max_length=100)
    body = models.TextField()
    summary = models.TextField(max_length=_summary_length, blank=True)
    images = models.ManyToManyField('Image', related_name='posts')
    publish_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    tags = models.ManyToManyField('Tag', related_name='posts')
    author = models.ForeignKey('Author', related_name='posts', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=_SLUG_LENGTH, unique=True, blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:_SLUG_LENGTH]
            if self.slug.endswith('-'):
                self.slug = self.slug[:-1]

        if not self.summary:
            self.summary = self.body[:self._summary_length]

        super().save(**kwargs)


class Author(models.Model):
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    display_name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=_SLUG_LENGTH, unique=True)

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('blog:author-post-list', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=_SLUG_LENGTH, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category-post-list', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=_SLUG_LENGTH, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag-post-list', kwargs={'slug': self.slug})


class Image(models.Model):
    title = models.CharField(max_length=100)
    alt_text = models.CharField(max_length=100)
    slug = models.SlugField(max_length=_SLUG_LENGTH, unique=True)
    image = models.ImageField(upload_to=_image_save_name)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:image-detail', kwargs={'slug': self.slug})

    def delete(self, *args, **kwargs):
        Path(self.image.path).unlink()
        super().delete(*args, **kwargs)
