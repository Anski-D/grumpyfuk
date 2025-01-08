import hashlib
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from django.conf import settings

_SLUG_LENGTH = 64


def _get_image_save_name(instance, filename):
    suffix = Path(filename).suffix

    return f'images/{timezone.now().strftime("%Y%m%d%H%M%S")}-{instance.image_hash}{suffix}'


def _get_image_hash(image):
    return hashlib.sha1(image.file.read()).hexdigest()


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

        super().save(*args, **kwargs)


class Author(models.Model):
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    display_name = models.CharField(max_length=36)
    slug = models.SlugField(max_length=_SLUG_LENGTH, unique=True)

    def __str__(self):
        return self.display_name

    @property
    def name(self):
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
    image = models.ImageField(upload_to=_get_image_save_name)
    image_hash = models.CharField(max_length=40, editable=False)
    image_path = models.CharField(max_length=1000, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:image-file', kwargs={'slug': self.slug})

    def delete(self, *args, **kwargs):
        Path(self.image.path).unlink()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if (image_hash := _get_image_hash(self.image)) != self.image_hash:
            if self.image_path:
                Path(settings.MEDIA_ROOT, self.image_path).unlink()
            self.image_hash = image_hash
            super().save(*args, **kwargs)
            self.image_path = self.image.name

        super().save(*args, **kwargs)


class DestinationType(models.TextChoices):
    CATEGORY = 'C', 'Category'
    POST = 'P', 'Post'
    TAG = 'T', 'Tag'


class InternalLink(models.Model):
    post = models.ForeignKey(Post, related_name='links', on_delete=models.CASCADE)

    destination_type = models.CharField(
        choices=DestinationType.choices,
        max_length=1,
        default=DestinationType.POST,
    )
    destination_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    destination_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    destination_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def destination(self):
        for destination in [self.destination_category, self.destination_post, self.destination_tag]:
            if destination is not None:
                return destination

    def __str__(self):
        return str(self.pk)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        models.Q(destination_type=DestinationType.CATEGORY, destination_post__isnull=True, destination_tag__isnull=True) |
                        models.Q(destination_type=DestinationType.POST, destination_category__isnull=True, destination_tag__isnull=True) |
                        models.Q(destination_type=DestinationType.TAG, destination_category__isnull=True, destination_post__isnull=True)
                ),
                name='%(app_label)s_%(class)s_only_one_destination',
            )
        ]

    def save(self, *args, **kwargs):
        destination_types = {key.casefold(): value for value, key in DestinationType.choices}
        self.destination_type = destination_types[self.destination._meta.verbose_name]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.destination.get_absolute_url()
