import markdown
from django.urls import reverse
from django.conf import settings
from markdown.inlinepatterns import LinkInlineProcessor, LINK_RE, ImageInlineProcessor, IMAGE_LINK_RE

from .models import InternalLink


class CustomFieldLinkInlineProcessor(LinkInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if any(href.startswith(start) for start in ['slug', 'pk']):
            key, app, name, slug = href.split(':')
            if key == 'pk':
                slug = InternalLink.objects.get(pk=slug).destination.slug
                
            relative_url = reverse(f'{app}:{name}', args=[slug])
            href = relative_url

        return href, title, index, handled


class ImageFieldImageInlineProcessor(ImageInlineProcessor):
    def getLink(self, data, index):
        src, title, index, handled = super().getLink(data, index)
        if src.startswith('slug'):
            _, app, name, slug = src.split(':')
            relative_url = reverse(f'{app}:{name}', args=[slug])
            src = relative_url
            if not settings.DEBUG:
                src = f'/cdn-cgi/image/fit=scale-down,width=auto{src}'

        return src, title, index, handled


class CustomSlugFieldExtensions(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwargs):
        md.inlinePatterns.register(
            CustomFieldLinkInlineProcessor(LINK_RE, md), 'link', 160
        )
        md.inlinePatterns.register(
            ImageFieldImageInlineProcessor(IMAGE_LINK_RE, md), 'image', 160
        )
