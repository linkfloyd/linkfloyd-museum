from django.conf.urls.defaults import patterns, url

from preferences.views import update

urlpatterns = patterns('',
    url(r'^update', update, name='update_preferences'),
)
