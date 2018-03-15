from django.shortcuts import render
from django.http import Http404

from dispatch.models import Article

def homepage(request):
    news =  Article.objects.filter(section__slug='news', is_published=True).order_by('-published_at')
    lifestyle = Article.objects.filter(section__slug='life', is_published=True).order_by('-published_at')
    features = Article.objects.filter(section__slug='features', is_published=True).order_by('-published_at')
    arts = Article.objects.filter(section__slug='arts', is_published=True).order_by('-published_at')
    sports = Article.objects.filter(section__slug='sports', is_published=True).order_by('-published_at')
    opinions = Article.objects.filter(section__slug='opinions', is_published=True).order_by('-published_at')

    context = {
        'news': news,
        'lifestyle': lifestyle,
        'features': features,
        'arts': arts,
        'sports': sports,
        'opinions': opinions,
        'footer': get_footer_context()
    }

    return render(request, 'homepage.html', context)

def section(request, slug=None):
    context = {}
    return render(request, 'section.html', context)

def article(request, year=0, month=0, slug=None):
    year, month = int(year), int(month)

    try:
        article = Article.objects.get(slug=slug, is_published=True)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    if article.published_at.year != year or article.published_at.month != month:
        raise Http404("Article does not exist")

    related = Article.objects \
        .filter(section=article.section, is_published=True) \
        .order_by('-published_at') \
        .exclude(id__in=[article.id])[:3]

    context = {
        'article': article,
        'related': related
    }

    return render(request, 'article.html', context)

def page(request, slug=None):
    context = {}
    return render(request, 'page.html', context)

def get_footer_context():
    sections = ['news', 'life', 'features', 'arts', 'sports', 'opinions']
    topics = {}

    for section in sections:
        print Article.objects \
                    .filter(is_published=True, section__slug=section) \
                    .values('topic') \
                    .distinct()
