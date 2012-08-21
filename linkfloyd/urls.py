from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

from django.views.generic.simple import direct_to_template
print settings.DEBUG
urlpatterns = patterns('',
    url(r'^$', 'links.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include('linkfloyd.links.urls')),
    url(r'^channels/', include('linkfloyd.channels.urls')),
    url(r'^comments/', include('linkfloyd.comments.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^preferences/', include('preferences.urls')),
    url(r'^wiki/', include('wiki.urls')),
    url(r'^api/', include('linkfloyd.api.urls')),
    url(r'^404/$', direct_to_template, {'template': '404.html'}),
    url(r'^500/$', direct_to_template, {'template': '500.html'}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
)

urlpatterns += staticfiles_urlpatterns()

"""
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
"""
