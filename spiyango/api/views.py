from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from spiyango.utils import get_info
from spiyango.links.models import Link, Channel

from gravatar import make as gravatar

def fetch_info(request):
    if request.GET.has_key("url"):
        return HttpResponse(
            simplejson.dumps(get_info(request.GET['url'])),
            'application/javascript')
    else:
        return HttpResponse(status=400)

@login_required
def delete_link(request):
    if request.GET.has_key("object_id"):
        try:
            link = Link.objects.get(
                pk=request.GET['object_id'], posted_by=request.user)
        except Link.DoesNotExist:
            return HttpResponse(status=404)
        link.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@login_required
def subscribe(request):
    if request.GET.has_key("channel_id"):
        try:
            channel = Channel.objects.get(pk=request.GET['channel_id'])
        except Channel.DoesNotExist:
            return HttpResponse(status=404)
        if not channel.subscribers.filter(id=request.user.id):
            channel.subscribers.add(request.user.id)
            return HttpResponse(
                simplejson.dumps({
                    "status": "subscribed",
                    "subscriber": {
                        "username": request.user.username,
                        "gravatar": gravatar(request.user.email, size=30)
                    },
                    "channel": {
                        "name": channel.title
                    }
                }, 'application/javascript'))
        else:
            channel.subscribers.remove(request.user.id)
            return HttpResponse(
                simplejson.dumps({
                    "status": "unsubscribed",
                    "subscriber": {
                        "username": request.user.username,
                        "gravatar": gravatar(request.user.email, size=30)
                    },
                    "channel": {
                        "name": channel.title
                    }
                }, 'application/javascript'))
    else:
        return HttpResponse(status=400)


def channels_list(request):

    from django.utils.translation import get_language as langcode

    query_string = request.GET.get("q", False)
    if query_string:
        channels = Channel.objects.filter(name__contains=query_string)
    else:
        channels = Channel.objects.all()

    response = []

    for c in channels:
        response.append({"id": c.id, "name": c.name })

    return HttpResponse(
        simplejson.dumps(response, 'application/javascript')
    )

@login_required
def post_report(request):
    from links.forms import SubmitReportForm

    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    if request.POST:
        print request.POST
        form = SubmitReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)
