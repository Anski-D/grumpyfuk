from django.contrib import admin

from .models import Post, Author, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
