from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^fetch_info/$', 'spiyango.api.views.fetch_info', name='fetch-info'),
    url(r'^channels/list/$', 'spiyango.api.views.channels_list', name='channels-list'),

    url(r'^links/delete/$', 'spiyango.api.views.delete_link', name='delete-link'),
    url(r'^reports/post/$', 'spiyango.api.views.post_report', name='post_report'),
    url(r'^votes/', include('qhonuskan_votes.urls'))
)
