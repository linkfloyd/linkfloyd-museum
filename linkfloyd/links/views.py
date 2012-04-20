from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.models import User

from qhonuskan_votes.models import vote_changed

from channels.models import Subscription

from links.models import Link, Channel, Report
from links.utils import context_builder
from links.forms import SubmitLinkForm, EditLinkForm

from comments.forms import CommentForm

from preferences.models import UserPreferences

@login_required
def submit_link(request):
    if request.method == "POST":
        form = SubmitLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.posted_by = request.user
            link.save()
            return HttpResponseRedirect("%s?highlight=%s" % (
                link.channel.get_absolute_url(), link.id))
        else:
            return render_to_response(
                "links/submit.html", {
                    "form": form,
                    "active_nav_item": "submit"
                }, context_instance=RequestContext(request))
    else:
        channel_slug = request.GET.get("channel")
        if channel_slug:
            channel = get_object_or_404(Channel, slug=channel_slug)
        else:
            channel = False
        return render_to_response(
            "links/submit.html", {
                "form": SubmitLinkForm(),
                "channel": channel,
                "active_nav_item": "submit"
            }, context_instance=RequestContext(request))

@login_required
def update(request, pk):
    if request.POST:
        form = EditLinkForm(
            request.POST,
            instance=get_object_or_404(Link, pk=pk, posted_by=request.user))
        if form.is_valid():
            link = form.save(request.POST)
            return HttpResponseRedirect(link.get_absolute_url())
        else:
            return render_to_response("links/submit.html", {
                "form": form
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("links/submit.html", {
            "form": EditLinkForm(
                instance=get_object_or_404(
                    Link, pk=pk, posted_by=request.user)),
            }, context_instance=RequestContext(request)
        )

def link_detail(request, link_id):
    try:
        link = Link.objects.get(id=link_id)
    except Link.DoesNotExist:
        return HttpResponse(status=404)
    link.inc_shown()
    return render_to_response("links/link_detail.html",
    {
        "link": link,
        "form": CommentForm(initial={"link": link})
    }, context_instance=RequestContext(request))


def index(request):
    if request.user.is_authenticated():
        if not Subscription.objects.filter(user=request.user):
            messages.add_message(request, messages.WARNING,
                "Please subscribe channels that you are interested in")
            return HttpResponseRedirect(reverse("browse_channels"))
    return render_to_response(
        "links/link_list.html",
        context_builder(request, links_from="subscriptions"),
        context_instance=RequestContext(request)
    )

def links_from_user(request, username):
    user = get_object_or_404(User, username=username)
    context = context_builder(request, links_from="user", instance=user)

    context.update({
        "about_user": UserPreferences.objects.get(user=user).description})

    return render_to_response(
        "links/link_list.html", context,
        context_instance=RequestContext(request)
    )

def links_from_channel(request, channel_slug):
    return render_to_response(
        "links/link_list.html",
        context_builder(request, links_from="channel",
            instance=get_object_or_404(Channel, slug=channel_slug)),
        context_instance=RequestContext(request)
    )


