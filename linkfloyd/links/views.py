from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

from channels.models import Subscription

from links.models import Link, Channel
from links.utils import context_builder
from links.forms import SubmitLinkForm, UpdateLinkForm

from comments.forms import CommentForm

from preferences.models import UserPreferences

from django.utils.translation import ugettext as _


@login_required
def submit_link(request, bookmarklet=False):

    if bookmarklet:
        template = "links/bookmarklet.html"
    else:
        template = "links/submit.html"

    if request.method == "POST":
        form = SubmitLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.posted_by = request.user
            link.save()
            if bookmarklet:
                return HttpResponse("<script>window.close()</script>")
            else:
                return HttpResponseRedirect("%s?highlight=%s" % (
                    link.channel.get_absolute_url(), link.id))
        else:
            print form.errors
            return render_to_response(
                template, {
                    "form": form,
                    "attachment_editable": True,
                    "active_nav_item": "submit"
                }, context_instance=RequestContext(request))
    else:
        channel_slug = request.GET.get("channel")
        if channel_slug:
            channel = get_object_or_404(Channel, slug=channel_slug)
        else:
            channel = False
        return render_to_response(
            template, {
                "form": SubmitLinkForm(initial={
                    "url": request.GET.get("url"),
                    "channel": channel,
                    "rating": 1
                }),
                "channel": channel,
                "attachment_editable": True,
                "active_nav_item": "submit"
            }, context_instance=RequestContext(request)
        )

@login_required
def update(request, pk):
    if request.POST:
        print request.POST
        form = UpdateLinkForm(
            request.POST,
            instance=get_object_or_404(
                Link, pk=pk, posted_by=request.user)
        )
        if form.is_valid():
            link = form.save(request.POST)
            return HttpResponseRedirect(link.get_absolute_url())
        else:
            print form.errors
            return render_to_response("links/submit.html", {
                "form": form,
                "attachment_editable": True
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("links/submit.html", {
                "form": UpdateLinkForm(
                    instance=get_object_or_404(
                        Link, pk=pk, posted_by=request.user)),
                "attachment_editable": True
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
        "up_voted_users": [vote.voter for vote in \
                           link.linkvote_set.filter(value=1)],
        "expanded_attachments": True,
        "expanded_comments": True,
        "form": CommentForm(initial={"link": link})
    }, context_instance=RequestContext(request))


def index(request):
    if request.user.is_authenticated():
        if not Subscription.objects.filter(user=request.user):
            messages.add_message(request, messages.WARNING,
                _("Subscribe channels that you are interested in"))
            return HttpResponseRedirect(reverse("browse_channels"))
    return render_to_response(
        "links/link_list.html",
        context_builder(request, links_from="subscriptions"),
        context_instance=RequestContext(request)
    )

def links_from_user(request, username):

    # Here were monkeypatching user instance to make it work with django_ogp

    user = get_object_or_404(User, username=username)
    description = UserPreferences.objects.get(user=user).description

    user.ogp_enabled = True
    user.ogp_title = _("%s on Linkfloyd" % user.username)
    user.ogp_description = description or ""

    # Prepare context
    context = context_builder(request, links_from="user", instance=user)
    context.update({"description": description})

    return render_to_response(
        "links/link_list.html", context,
        context_instance=RequestContext(request))

def links_upvoted_by_user(request, username):

    # Here were monkeypatching user instance to make it work with
    # django_ogp

    user = get_object_or_404(User, username=username)
    description = UserPreferences.objects.get(user=user).description

    user.ogp_enabled = True
    user.ogp_title = _("%s's Up Votes on Linkfloyd" % user.username)
    user.ogp_description = description or ""

    # Prepare context
    context = context_builder(request, links_from="likes", instance=user)
    context.update({"description": description})

    return render_to_response(
        "links/link_list.html", context,
        context_instance=RequestContext(request))

def links_from_all_channels(request):
    context = context_builder(request)
    return render_to_response(
        "links/link_list.html", context,
        context_instance=RequestContext(request))


def links_from_channel(request, channel_slug):
    channel = get_object_or_404(Channel, slug=channel_slug)
    context = context_builder(request, links_from="channel", instance=channel)
    context.update({
        "sibling_channels": Channel.objects.filter(
            parent=channel.parent) if channel.parent else None,
        "child_channels": Channel.objects.filter(parent=channel)})
    return render_to_response(
        "links/link_list.html", context,
        context_instance=RequestContext(request)
    )

def random(request):
    link = Link.objects.order_by('?')[0]
    return HttpResponseRedirect(link.get_absolute_url())
