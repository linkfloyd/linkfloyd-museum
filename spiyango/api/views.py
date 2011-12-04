# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from spiyango.utils import get_info
from django.contrib.auth.decorators import login_required
from spiyango.links.models import Link, Channel

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


def channels_list(request):

    from django.utils.translation import get_language as langcode

    query_string = request.GET.get("q", False)
    if query_string:
        kwargs = {"title_%s__contains" % langcode() : query_string}
        channels = Channel.objects.filter(**kwargs)
    else:
        channels = Channel.objects.all()

    response = []

    for c in channels:
        response.append({"id": c.id, "name": c.title })

    return HttpResponse(
        simplejson.dumps(response, 'application/javascript')
    )
