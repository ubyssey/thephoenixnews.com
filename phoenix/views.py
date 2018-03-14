from django.shortcuts import render
from django.http import Http404

from dispatch.models import Article

def homepage(request):
    featured = Article.objects.filter(importance=5, is_published=True).order_by('-published_at')[0]
    news =  Article.objects.filter(section__slug='news', is_published=True).order_by('-published_at')

    context = {
        'featured': featured,
        'news': news
    }

    return render(request, 'homepage.html', context)

def section(request):
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

    context = {
        'article': article
    }

    return render(request, 'article.html', context)

def page(request):
    context = {}
    return render(request, 'page.html', context)
