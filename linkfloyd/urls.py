from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from linkfloyd.api import LinkResource

v1_api = Api(api_name='v1')
v1_api.register(LinkResource())

admin.autodiscover()

from django.views.generic.simple import direct_to_template

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
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/img/favicon.ico'}),
    url(r'^restful/', include(v1_api.urls)),
    url(r'^palette/$', direct_to_template, {'template': 'palette_test.html'})
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
