# Create your views here.

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from notifications.models import Notification


def list(request):

    objects = []
    notifications = Notification.objects.filter(recipient=request.user).order_by("-date")

    for i in xrange(10):
        objects.append({
            "sentence": render_to_string(
                "notifications/%s/sentence.html" % notifications[i].type.label, {
                    "notification": notifications[i]}),
            "date": notifications[i].date
        })
    notifications.update(seen=True)
    notifications[10:].delete()
    return render_to_response("notifications/list.html",
            {"objects": objects})
