from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^fetch_info/$', 'linkfloyd.api.views.fetch_info', name='fetch-info'),
    url(r'^channels/list/$', 'linkfloyd.api.views.channels_list', name='channels_list'),
    url(r'^links/delete/$', 'linkfloyd.api.views.delete_link', name='delete_link'),
    url(r'^comments/delete/$', 'linkfloyd.api.views.delete_comment', name='delete_comment'),
    url(r'^reports/post/$', 'linkfloyd.api.views.post_report', name='post_report'),
    url(r'^votes/', include('qhonuskan_votes.urls'))
)
