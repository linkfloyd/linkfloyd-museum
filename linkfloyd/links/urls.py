from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^from/(?P<username>\w+)/$', 'links.views.links_from_user', name='links_from_user'),
    url(r'^liked/(?P<username>\w+)/$', 'links.views.links_upvoted_by_user', name='links_upvoted_by'),

    url(r'^all/$', 'links.views.links_from_all_channels', name='all_links'),
    
    url(r'^channel/(?P<channel_slug>[-\w+]+)/$', 'links.views.links_from_channel', name='links_from_channel'),
    url(r'^submit/$', 'linkfloyd.links.views.submit_link', name='submit_link'),
    url(r'^bookmark/', 'linkfloyd.links.views.submit_link', {"bookmarklet":True}, name="bookmark_link"),

    url(r'^update/(?P<pk>\d+)/$', 'linkfloyd.links.views.update', name='update_link'),
    url(r'^random/$', 'linkfloyd.links.views.random', name='random_link'),
    url(r'^(?P<link_id>\d+)/$', 'linkfloyd.links.views.link_detail', name='show_link'),
)

