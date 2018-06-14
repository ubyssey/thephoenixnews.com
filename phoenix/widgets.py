from dispatch.theme import register
from dispatch.theme.widgets import Zone, Widget
from dispatch.theme.fields import ArticleField, TopicField

@register.zone
class HomepageZone(Zone):
    id = 'homepage'
    name = 'Homepage'

@register.zone
class NewsZone(Zone):
    id = 'news'
    name = 'News'

@register.zone
class LifeZone(Zone):
    id = 'life'
    name = 'Life'

@register.zone
class FeaturesZone(Zone):
    id = 'features'
    name = 'Features'

@register.zone
class ArtsZone(Zone):
    id = 'arts'
    name = 'Arts'

@register.zone
class SportsZone(Zone):
    id = 'sports'
    name = 'Sports'

@register.zone
class OpinionsZone(Zone):
    id = 'opinions'
    name = 'Opinions'

@register.widget
class FeaturedArticle(Widget):
    id = 'featured-article'
    name = 'Featured Article'

    zones = (HomepageZone,)
    template = 'components/article-banner.html'

    article = ArticleField('Article')

@register.widget
class TopicsWidget(Widget):
    id = 'topics'
    name = 'Topics'
    template = 'components/topics.html'

    zones = (NewsZone, LifeZone, FeaturesZone, ArtsZone, SportsZone, OpinionsZone)
    accepted_keywords = ('section', 'current_topic')

    topics = TopicField('Topics', many=True)
