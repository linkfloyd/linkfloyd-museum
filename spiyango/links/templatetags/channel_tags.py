from django import template
from channels.models import Subscription
register = template.Library()

@register.filter
def is_following(user, channel):
    if not user.is_authenticated():
        return bool(Subscription.objects.filter(user=user, channel=channel).count())
    else:
        return False
