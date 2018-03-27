from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from dispatch.models import Article, Section, Topic

def homepage(request):
    news =  Article.objects.filter(section__slug='news', is_published=True).order_by('-published_at')
    lifestyle = Article.objects.filter(section__slug='life', is_published=True).order_by('-published_at')
    features = Article.objects.filter(section__slug='features', is_published=True).order_by('-published_at')
    arts = Article.objects.filter(section__slug='arts', is_published=True).order_by('-published_at')
    sports = Article.objects.filter(section__slug='sports', is_published=True).order_by('-published_at')
    opinions = Article.objects.filter(section__slug='opinions', is_published=True).order_by('-published_at')

    context = {
        'title': 'The Phoenix - UBCO\'s student newspaper',
        'news': news,
        'lifestyle': lifestyle,
        'features': features,
        'arts': arts,
        'sports': sports,
        'opinions': opinions,
        'footer': get_footer_context()
    }

    return render(request, 'homepage.html', context)

def section_home(request, slug=None):
    return section(request, slug, None)

def section_topic(request, slug=None, topic=None):
    return section(request, slug, topic)

def section(request, section_slug=None, topic_slug=None):

    try:
        section = Section.objects.get(slug=section_slug)
    except Section.DoesNotExist:
        raise Http404("Section does not exist")

    articles = Article.objects \
        .filter(is_published=True, section=section) \
        .order_by('-published_at')

    if topic_slug:
        try:
            topic = Topic.objects.get(slug=topic_slug)
        except Topic.DoesNotExist:
            raise Http404("Topic does not exist")

        articles = articles.filter(topic=topic)
    else:
        topic = None

    paginator = Paginator(articles[4:], 15)
    page = request.GET.get('page')

    try:
        archive = paginator.page(page)
    except PageNotAnInteger:
        archive = paginator.page(1)
    except EmptyPage:
        archive = paginator.page(paginator.num_pages)

    context = {
        'title': '%s - The Phoenix' % section.name,
        'section': section,
        'topic': topic,
        'articles': {
            'primary': articles[0],
            'secondary': articles[1:4],
            'archive': archive
        }
    }

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
        'title': '%s - The Phoenix' % article.headline,
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
