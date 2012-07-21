from django.conf.urls.defaults import patterns, include, url
from channels.views import BrowseChannelsView, SubscriptionsView

urlpatterns = patterns('',
    url(r'^create/$',
        'linkfloyd.channels.views.create', name='create_channel'),
 
    url(r'^update/(?P<slug>[-\w+]+)/$',
        'linkfloyd.channels.views.update', name='update_channel'),

    url(r'^browse/$',
        BrowseChannelsView.as_view(), name='browse_channels'),

    url(r'^subscriptions/$',
        SubscriptionsView.as_view(), name='browse_subscriptions'),

)
