# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from spiyango.utils import get_info
from django.contrib.auth.decorators import login_required
from spiyango.links.models import Link

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


