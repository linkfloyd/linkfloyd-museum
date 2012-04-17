from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^submit/$', 'comments.views.submit', name='submit_comment'),
    url(r'^update/(?P<pk>\d+)/$', 'comments.views.update', name='update_comment'),
)
