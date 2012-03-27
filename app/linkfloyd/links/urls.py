from django.conf.urls.defaults import patterns, url

from linkfloyd.links.views import LinksFromUserView
from linkfloyd.links.views import LinksFromChannelView
from linkfloyd.links.views import LatestLinksView

urlpatterns = patterns('',
    url(r'^from/(?P<user>\w+)/$', LinksFromUserView.as_view(), name='links_from_user'),
    url(r'^channel/(?P<channel>[-\w+]+)/$', LinksFromChannelView.as_view(), name='links_from_channel'),
    url(r'^latest/$', LatestLinksView.as_view(), name='latest_links'),
    url(r'^submit/$', 'linkfloyd.links.views.submit_link', name='submit_link'),
    url(r'^update/(?P<pk>\d+)/$', 'linkfloyd.links.views.update', name='update_link'),
    url(r'^(?P<link_id>\d+)/$', 'linkfloyd.links.views.link_detail', name='show_link'),
)
