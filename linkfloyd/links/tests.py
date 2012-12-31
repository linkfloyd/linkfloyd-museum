from django.test import TestCase
from channels.models import Channel
from links.models import Link
from django.contrib.auth.models import User
from qhonuskan_votes.utils import get_vote_model
from datetime import datetime, timedelta
from links.utils import context_builder
from django.core.handlers.base import BaseHandler  
from django.test.client import RequestFactory  
  

class RequestMock(RequestFactory):  
    def request(self, **request):  
        "Construct a generic request object."  
        request = RequestFactory.request(self, **request)  
        handler = BaseHandler()  
        handler.load_middleware()  
        for middleware_method in handler._request_middleware:  
            if middleware_method(request):  
                raise Exception("Couldn't create request mock object - "  
                                "request middleware returned a response")  
        return request  


class ContextBuilderTest(TestCase):
    fixtures = [
        'fixtures/languages.yaml',
        'fixtures/notificationtypes.yaml',
        'fixtures/users_test_data.yaml',
        'fixtures/channels_test_data.yaml'
    ]

    def setUp(self):
        self.users = User.objects.all()
        self.channels = Channel.objects.all()
        self.links = [
            # A link posted today
            Link.objects.create(
                posted_by=self.users[0],
                body="Link1",
                url="http://www.google.com",
                channel=self.channels[0],
                posted_at=datetime.now()
            ),
            # A link posted yesterday
            Link.objects.create(
                posted_by = self.users[0],
                body="Link1",
                url="http://www.google.com",
                channel=Channel.objects.get(pk=1),
                posted_at=datetime.now() - timedelta(days=1)
            ),
            # A link posted two days ago
            Link.objects.create(
                posted_by = self.users[0],
                body="Link1",
                url="http://www.google.com",
                channel=Channel.objects.get(pk=1),
                posted_at=datetime.now() - timedelta(days=2)
            )
        ]

    def test_all_links(self):
    	request = RequestMock().request()
    	self.assertQuerysetEqual(context_builder(request)['links'], Link.objects.all())
