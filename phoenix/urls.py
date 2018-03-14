from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.shortcuts import render_to_response

from dispatch.admin import urls as admin_urls
from dispatch.api import urls as api_urls

from phoenix import views

urlpatterns = [
    url(r'^admin', include(admin_urls)),
    url(r'^api/', include(api_urls)),

    url(r'^$', views.homepage, name='homepage'),
    url(r'^section/$', views.section, name='section'),
    url(r'^page/$', views.page, name='page'),

    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[-\w]+)/$', views.article, name='article'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
