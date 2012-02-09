from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

from links.views import LinksListView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', LinksListView.as_view(), name='link_list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include('linkfloyd.links.urls')),
    url(r'^channels/', include('linkfloyd.channels.urls')),
    url(r'^api/', include('linkfloyd.api.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^preferences/', include('preferences.urls')),
    url(r'^invite/', include('privatebeta.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
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
        })
    )
