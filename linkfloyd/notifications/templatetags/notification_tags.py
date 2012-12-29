# -*- coding: utf-8 -*-
from django.template import Library
from notifications.models import Notification

register = Library()


@register.assignment_tag(takes_context=True)
def get_unread_notifications_count(context):
    if 'user' not in context:
        return ''

    user = context['user']

    if user.is_anonymous():
        return ''

    return Notification.objects.filter(recipient=user,
        seen=False).count()
