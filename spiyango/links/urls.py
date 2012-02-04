
from django.conf.urls.defaults import patterns, url

from spiyango.links.views import LinkDetail
from spiyango.links.views import LinksFromUserView
from spiyango.links.views import LinksFromChannelView
from spiyango.links.views import LatestLinksView

urlpatterns = patterns('',
    url(r'^from/(?P<user>\w+)/$', LinksFromUserView.as_view(), name='links_from_user'),
    url(r'^channel/(?P<channel>[-\w+]+)/$', LinksFromChannelView.as_view(), name='links_from_channel'),
    url(r'^latest/$', LatestLinksView.as_view(), name='latest_links'),
    url(r'^submit/$', 'spiyango.links.views.submit', name='submit_link'),
    url(r'^edit/(?P<pk>\d+)/$', 'spiyango.links.views.edit', name='edit_link'),
    url(r'^(?P<pk>\d+)/$', LinkDetail.as_view(), name='show_link'),
)
