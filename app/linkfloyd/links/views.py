from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import  ListView
from django.contrib import messages

from channels.models import Subscription
from links.models import Link, Channel, Report
from links.utils import query_builder

from links.forms import SubmitLinkForm, EditLinkForm
from comments.forms import SubmitCommentForm

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
def edit(request, pk):
    if request.POST:
        form = EditLinkForm(
            request.POST,
            instance=get_object_or_404(Link, pk=pk, posted_by=request.user))
        if form.is_valid():
            link = form.save(request.POST)
            return HttpResponseRedirect(link.get_absolute_url())
        else:
            return render_to_response("links/edit.html", {
                "form": form
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("links/edit.html", {
            "form": EditLinkForm(
                instance=get_object_or_404(
                    Link, pk=pk, posted_by=request.user)),
            }, context_instance=RequestContext(request)
        )

def link_detail(request, link_id):

    link = get_object_or_404(Link, id=link_id)
    link.inc_shown()
    return render_to_response("links/link_detail.html",
    {
        "link": link,
        "form": SubmitCommentForm(initial={"link": link})
    }, context_instance=RequestContext(request))


class LinksListView(ListView):
    context_object_name = "links"
    paginate_by = 20

    def get_queryset(self):
        return query_builder(self.request)

    def get_context_data(self, **kwargs):
        context = super(LinksListView, self).get_context_data(**kwargs)

        if "highlight" in self.request.GET:
            context['highlight'] = int(self.request.GET['highlight'])

        context['active_nav_item'] = "links"
        return context

class IndexView(LinksListView):

    def get_queryset(self):
        return query_builder(
            self.request, from_subscriptions=True)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['listing_title'] = "Links From Your Subscripted Channels"
        return context

    def render_to_response(self, context):
        if (not Subscription.objects.filter(user=self.request.user).count() and
                self.request.user.is_authenticated()):
            messages.add_message(self.request, messages.WARNING,
                "Please subscribe channels that you are interested in")
            return HttpResponseRedirect(reverse("browse_channels"))
        return super(IndexView, self).render_to_response(context)


class LatestLinksView(LinksListView):
    def get_queryset(self):
        return query_builder(self.request, order_by="-posted_at")

    def get_context_data(self, **kwargs):
        context = super(LatestLinksView, self).get_context_data(**kwargs)
        context['listing_title'] = "Latest Links"
        return context

class LinksFromUserView(LinksListView):
    def get_queryset(self):
        return query_builder(self.request, user=self.kwargs["user"])

    def get_context_data(self, **kwargs):
        context = super(LinksFromUserView, self).get_context_data(**kwargs)
        context['listing_title'] = "Links From %s" % self.kwargs["user"]
        context['profile'] = get_object_or_404(
            UserPreferences, user__username = self.kwargs["user"])
        return context

class LinksFromChannelView(LinksListView):
    def get_queryset(self):
        return query_builder(self.request, channel=self.kwargs["channel"])

    def get_context_data(self, **kwargs):

        context = super(LinksFromChannelView, self).get_context_data(**kwargs)
        channel = get_object_or_404(Channel, slug=self.kwargs["channel"])
        context['listing_title'] = "Links From %s Channel" % channel
        context['channel'] = channel
        return context
