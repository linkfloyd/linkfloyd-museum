from django.conf.urls.defaults import patterns, include, url
from channels.views import BrowseChannelsView

urlpatterns = patterns('',
    url(r'^create/$', 'spiyango.channels.views.create', name='create_channel'),
    url(r'^subscribe/(?P<slug>[-\w+]+)/$', 'spiyango.channels.views.subscribe', name='subscibe_channel'),
    url(r'^unsubscribe/(?P<slug>[-\w+]+)/$', 'spiyango.channels.views.unsubscribe', name='unsubscibe_channel'),
    url(r'^browse/$', BrowseChannelsView.as_view(), name='browse_channels'),

)
