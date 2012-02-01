from django import template
from channels.models import Subscription
register = template.Library()

@register.filter
def is_following(user, channel):
    return bool(Subscription.objects.filter(user=user, channel=channel).count())
