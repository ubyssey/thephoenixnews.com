from dispatch.theme import register
from dispatch.theme.widgets import Zone, Widget
from dispatch.theme.fields import ArticleField

@register.zone
class HomepageZone(Zone):
    id = 'homepage'
    name = 'Homepage'

@register.widget
class FeaturedArticle(Widget):
    id = 'featured-article'
    name = 'Featured Article'

    zones = (HomepageZone,)
    template = 'components/article-banner.html'

    article = ArticleField('Article')
