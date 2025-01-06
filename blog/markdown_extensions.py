import markdown
from markdown.inlinepatterns import LinkInlineProcessor, LINK_RE, ImageInlineProcessor, IMAGE_LINK_RE

from django.conf import settings
from .models import InternalLink, Image


class InternalLinkFieldLinkInlineProcessor(LinkInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        href_parts = href.split(':')
        if href_parts[0] == 'internal-link':
            relative_url = InternalLink.objects.get(pk=href_parts[1]).get_absolute_url()
            href = relative_url

        return href, title, index, handled


class ImageFieldImageInlineProcessor(ImageInlineProcessor):
    def getLink(self, data, index):
        src, title, index, handled = super().getLink(data, index)
        src_parts = src.split(':')
        if src_parts[0] == 'image':
            relative_url = Image.objects.get(pk=src_parts[1]).get_absolute_url()
            src = relative_url
            if not settings.DEBUG:
                src = f'/cdn-cgi/image/fit=scale-down,width=auto,format=avif{src}'

        return src, title, index, handled


class LinkFieldExtensions(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwargs):
        md.inlinePatterns.register(
            InternalLinkFieldLinkInlineProcessor(LINK_RE, md), 'link', 160
        )
        md.inlinePatterns.register(
            ImageFieldImageInlineProcessor(IMAGE_LINK_RE, md), 'image', 160
        )
