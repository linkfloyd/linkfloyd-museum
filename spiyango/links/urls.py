
from django.conf.urls.defaults import patterns, include, url
from spiyango.links.models import Link

from spiyango.links.views import LatestLinksView, LinkDetail

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', LinkDetail.as_view(), name='show_link'),
    url(r'^submit/$', 'spiyango.links.views.submit', name='submit_link'),
    url(r'^edit/(?P<pk>\d+)/$', 'spiyango.links.views.edit', name='edit_link'),
    url(r'^latest/$', LatestLinksView.as_view(), name='latest_links')
)
