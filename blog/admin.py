from django.contrib import admin
from django.db.models import Count

from .models import Post, Author, Category, Tag, Image, InternalLink


class CommonAdmin(admin.ModelAdmin):
    @admin.display(description='Number of posts')
    def count_posts(self, obj):
        return obj.posts__count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(Count('posts'))

        return queryset


@admin.register(Image)
class ImageAdmin(CommonAdmin):
    list_display = ('title', 'count_posts')
    prepopulated_fields = {'slug': ('title',)}


class ImageInline(admin.TabularInline):
    model = Post.images.through
    extra = 0
    readonly_fields = ('image_id',)


class InternalLinksInline(admin.TabularInline):
    model = InternalLink
    fk_name = 'post'
    extra = 0
    readonly_fields = ('destination_type',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [InternalLinksInline, ImageInline]
    exclude = ('images',)


@admin.register(Author)
class AuthorAdmin(CommonAdmin):
    list_display = ('display_name', 'count_posts')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


@admin.register(Category)
class CategoryAdmin(CommonAdmin):
    list_display = ('name', 'count_posts')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(CommonAdmin):
    list_display = ('name', 'count_posts')
    prepopulated_fields = {'slug': ('name',)}
