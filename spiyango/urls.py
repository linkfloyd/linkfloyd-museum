from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

from links.views import TopLinksView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^((\w+)/)?$', TopLinksView.as_view(), name='top_links'),
    url(r'^links/', include('spiyango.links.urls')),
    url(r'^api/', include('spiyango.api.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
