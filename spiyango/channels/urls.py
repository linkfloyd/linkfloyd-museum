from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^create/$', 'spiyango.channels.views.create', name='create_channel'),
)
