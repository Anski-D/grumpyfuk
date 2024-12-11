import markdown
from django.urls import reverse
from markdown.inlinepatterns import LinkInlineProcessor, LINK_RE, ImageInlineProcessor, IMAGE_LINK_RE


class SlugFieldLinkInlineProcessor(LinkInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if href.startswith('slug'):
            _, app, name, slug = href.split(':')
            relative_url = reverse(f'{app}:{name}', args=[slug])
            href = relative_url

        return href, title, index, handled


class SlugFieldExtensions(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwargs):
        md.inlinePatterns.register(
            SlugFieldLinkInlineProcessor(LINK_RE, md), 'link', 160
        )


class ImageFieldImageInlineProcessor(ImageInlineProcessor):
    def getLink(self, data, index):
        src, title, index, handled = super().getLink(data, index)
        if src.startswith('slug'):
            _, app, name, slug = src.split(':')
            relative_url = reverse(f'{app}:{name}', args=[slug])
            src = relative_url

        return src, title, index, handled


class ImageFieldExtensions(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwargs):
        md.inlinePatterns.register(
            ImageFieldImageInlineProcessor(IMAGE_LINK_RE, md), 'image', 160
        )
