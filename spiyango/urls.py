from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

from links.views import LinksListView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', LinksListView.as_view(), name='link_list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include('spiyango.links.urls')),
    url(r'^channels/', include('spiyango.channels.urls')),
    url(r'^api/', include('spiyango.api.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^preferences/', include('preferences.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',  'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}))
