from django.conf.urls.defaults import patterns, include, url
from channels.views import BrowseChannelsView

urlpatterns = patterns('',
    url(r'^create/$', 'linkfloyd.channels.views.create', name='create_channel'),
    url(r'^update/(?P<slug>[-\w+]+)/$', 'linkfloyd.channels.views.update', name='update_channel'),
    url(r'^subscribe/(?P<slug>[-\w+]+)/$', 'linkfloyd.channels.views.subscribe', name='subscibe_channel'),
    url(r'^unsubscribe/(?P<slug>[-\w+]+)/$', 'linkfloyd.channels.views.unsubscribe', name='unsubscibe_channel'),
    url(r'^browse/$', BrowseChannelsView.as_view(), name='browse_channels'),

)
