from django.conf.urls import patterns, url
from linkfloyd.experimental.views import GetImages


urlpatterns = patterns(
    '',

    url('^$',
        view=GetImages.as_view(),
        name='experimental-get-images')
)
