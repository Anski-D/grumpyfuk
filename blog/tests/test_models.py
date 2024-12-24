from django.test import TestCase

from blog.models import Post, Category, Tag, Author


class PostModelTest(TestCase):
    _fields = {
        'title': 'title',
        'body': 'body',
        'summary': 'summary',
        'images': 'images',
        'publish_date': 'publish date',
        'last_updated': 'last updated',
        'categories': 'categories',
        'tags': 'tags',
        'author': 'author',
        'slug': 'slug',
        'published': 'published',
    }

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='CategoryTest', slug='categorytest')
        tag = Tag.objects.create(name='TagTest', slug='tagtest')
        author = Author.objects.create(
            first_name='FirstNameTest',
            last_name="LastNameTest",
            slug='firstnametest-lastnametest',
        )
        post = Post.objects.create(
            title='Post title',
            body='Post body',
            author = author,
        )
        post.categories.set([category])
        post.tags.set([tag])

    def test_labels(self):
        """Labels are correct."""
        post = Post.objects.get(id=1)
        for field, label in self._fields.items():
            with self.subTest(field=field, label=label):
                field_label = post._meta.get_field(field).verbose_name

                self.assertEqual(field_label, label)

    def test_get_absolute_url(self):
        """Absolute url is based on slug."""
        post = Post.objects.get(id=1)

        self.assertEqual(post.get_absolute_url(), '/blog/post/post-title/')
