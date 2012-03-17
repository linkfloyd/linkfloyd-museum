from django import template
from channels.models import Subscription

register = template.Library()

@register.filter
def is_following(user, channel):
    if user.is_authenticated():
        return bool(
            Subscription.objects.filter(user=user, channel=channel).count()
        )
    else:
        return False

@register.filter
def subscription_status(user, channel):
    if user.is_authenticated():
        try:
            subscription = Subscription.objects.get(
                user=user,
                channel=channel)
        except Subscription.DoesNotExists:
            subscription = None
        if subscription:
            return subscription.status
        else:
            return None
    else:
        return None
