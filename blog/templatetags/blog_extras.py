import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from blog.markdown_extensions import LinkFieldExtensions

register = template.Library()


@register.filter
@stringfilter
def render_markdown(value):
    md = markdown.Markdown(
        extensions=[
            'extra',
            LinkFieldExtensions(),
        ]
    )

    return mark_safe(md.convert(value))
