from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

from links.views import TopLinksView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include('spiyango.links.urls')),
    url(r'^api/', include('spiyango.api.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^((\w+)/)?$', TopLinksView.as_view(), name='top_links'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
