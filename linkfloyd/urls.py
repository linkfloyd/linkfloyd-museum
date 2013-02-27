from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from links.models import Link
from channels.models import Channel
from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
admin.autodiscover()


class LinkSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Link.objects.filter(is_draft=False)

    def lastmod(self, link):
        return link.updated_at


urlpatterns = patterns(
    '',

    url(r'^$', 'links.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include('linkfloyd.links.urls')),
    url(r'^channels/', include('linkfloyd.channels.urls')),
    url(r'^comments/', include('linkfloyd.comments.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^wiki/', include('wiki.urls')),
    url(r'^api/', include('linkfloyd.api.urls')),
    url(r'^preferences/', include('linkfloyd.preferences.urls')),
    url(r'^notifications/', 'linkfloyd.notifications.views.list'),
    url(r'^404/$', direct_to_template, {'template': '404.html'}),
    url(r'^500/$', direct_to_template, {'template': '500.html'}),
    url(r'^testpage/$', direct_to_template, {
        'template': 'testpage.html',
        'extra_context': {
            'links': Link.objects.all()[835:836],
            'channels': Channel.objects.all()[0:5],
            'expanded_comments': True,
            'expanded_attachment': True,
        }
    }),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/img/favicon.ico'}),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {
        'links': GenericSitemap({
            'queryset': Link.objects.all(),
            'priority': 0.6,
            'changefreq': "daily"
        })
    }})
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns(
        '',

        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {
             'document_root': settings.MEDIA_ROOT,
             'show_indexes': True
         }),
        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {
             'document_root': settings.STATIC_ROOT,
             'show_indexes': True
         }),
        #url(r'^experimental/', include('linkfloyd.experimental.urls'))
    )
