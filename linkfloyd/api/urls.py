from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^fetch_info/$',
         'linkfloyd.api.views.fetch_info',
         name='fetch-info'),

    url(r'^channels/list/$',
         'linkfloyd.api.views.channels_list',
         name='channels_list'),

    url(r'^channels/subscription/switch/$',
         'linkfloyd.api.views.switch_channel_subscription',
         name='subscribe_channel'),

    url(r'^links/subscription/switch/$',
         'linkfloyd.api.views.switch_link_subscription',
         name='subscribe_channel'),

    url(r'^links/delete/$',
         'linkfloyd.api.views.delete_link',
         name='delete_link'),

    url(r'^comments/delete/$',
         'linkfloyd.api.views.delete_comment',
         name='delete_comment'),

    url(r'^comments/get_form/$',
         'linkfloyd.api.views.get_update_comment_form',
         name='get_update_comment_form'),

    url(r'^votes/',
        include('qhonuskan_votes.urls'))
)
