from django.conf.urls.defaults import patterns, include, url
import django_votes.urls
urlpatterns = patterns('',
    url(r'^fetch_info/$', 'spiyango.api.views.fetch_info', name='fetch-info'),
    url(r'^links/delete/$', 'spiyango.api.views.delete_link', name='delete-link'),
    url(r'^votes/', include(django_votes.urls))
)
