from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^submit/$', 'comments.views.submit', name='submit_comment'),
)
