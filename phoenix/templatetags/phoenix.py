from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def article_url(article, **kwargs):
    """Generate url for given article."""

    year = '%04d' % article.published_at.year
    month = '%02d' % article.published_at.month
    slug = article.slug

    return reverse(
        'article',
        kwargs={'year': year, 'month': month, 'slug': slug}
    )

@register.simple_tag
def section_url(slug, **kwargs):
    """Generate url for given section."""

    return reverse(
        'section',
        kwargs={'slug': slug}
    )
