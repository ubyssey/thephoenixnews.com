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

@register.simple_tag
def topic_url(section_slug, topic_slug, **kwargs):
    """Generate url for given topic."""

    return reverse(
        'section-topic',
        kwargs={'slug': section_slug, 'topic': topic_slug}
    )

@register.simple_tag
def issue_url(issue, **kwargs):
    """Generate url for given issue."""
    return reverse(
        'issue',
        kwargs={
            'year': issue.date.strftime('%Y'),
            'month': issue.date.strftime('%m'),
            'day': issue.date.strftime('%d')
        }
    )

@register.simple_tag
def article_tag(article, **kwargs):
    """Return the primary tag for the given article."""

    if article.topic:
        return article.topic.name

    if article.tags.first():
        return article.tags.first().name

    return article.section.name
