from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from spiyango.utils import get_info
from spiyango.channels.models import Channel
from spiyango.links.models import Link, Comment

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
    if request.GET.has_key("id"):
        try:
            link = Link.objects.get(
                pk=request.GET['id'], posted_by=request.user)
        except Link.DoesNotExist:
            return HttpResponse(status=404)
        link.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@login_required
def delete_comment(request):
    if request.GET.has_key("id"):
        try:
            comment = Comment.objects.get(
                pk=request.GET['id'], posted_by=request.user)
        except Comment.DoesNotExist:
            return HttpResponse(status=404)
        comment.delete()
        return HttpResponse(status=200)
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
