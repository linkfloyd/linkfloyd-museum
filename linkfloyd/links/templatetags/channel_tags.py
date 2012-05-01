from django import template
from channels.models import Subscription as ChannelSubscription
from links.models import Subscription as LinkSubscription

register = template.Library()

@register.filter
def channel_subscription_status(user, channel):
    if user.is_authenticated():
        try:
            subscription = ChannelSubscription.objects.get(
                user=user,
                channel=channel)
        except ChannelSubscription.DoesNotExist:
            subscription = None
        if subscription:
            return subscription.status
        else:
            return None
    else:
        return None

@register.filter
def link_subscription_status(user, link):
    if user.is_authenticated():
        try:
            subscription = LinkSubscription.objects.get(
                user=user,
                link=link)
        except LinkSubscription.DoesNotExist:
            subscription = None

        if subscription:
            return subscription.status
        else:
            return False
    else:
        return False
