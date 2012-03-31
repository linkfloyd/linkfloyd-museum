from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^from/(?P<user>\w+)/$', 'links.views.links_from_user', name='links_from_user'),
    url(r'^channel/(?P<channel>[-\w+]+)/$', 'links.views.links_from_channel', name='links_from_channel'),
    url(r'^submit/$', 'linkfloyd.links.views.submit_link', name='submit_link'),
    url(r'^update/(?P<pk>\d+)/$', 'linkfloyd.links.views.update', name='update_link'),
    url(r'^(?P<link_id>\d+)/$', 'linkfloyd.links.views.link_detail', name='show_link'),
)

