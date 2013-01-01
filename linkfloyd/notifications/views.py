# Create your views here.

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from notifications.models import Notification


def list(request):

    objects = []
    notifications = Notification.objects.filter(recipient=request.user).order_by("-date")

    for notification in notifications:
        objects.append({
            "sentence": render_to_string(
                "notifications/%s/sentence.html" % notification.type.label, {
                    "notification": notification}),
            "date": notification.date
        })
    notifications.update(seen=True)
    return render_to_response("notifications/list.html",
            {"objects": objects})
