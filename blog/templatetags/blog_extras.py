import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from blog.markdown_extensions import SlugFieldExtensions

register = template.Library()


@register.filter
@stringfilter
def render_markdown(value):
    md = markdown.Markdown(extensions=['fenced_code', SlugFieldExtensions()])

    return mark_safe(md.convert(value))
