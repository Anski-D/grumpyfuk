from django.contrib import admin

from .models import Post, Author, Category, Tag, Comment


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
