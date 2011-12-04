# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Sum, Count

from datetime import datetime
from datetime import timedelta

from taggit.models import Tag

from spiyango.links.models import Link, Channel
from spiyango.links.forms import SubmitLinkForm, EditLinkForm

from django.db.models import Q

@login_required
def submit(request):
    if request.POST:
        print request.POST
        form = SubmitLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.posted_by = request.user
            link.save()
            return HttpResponseRedirect(link.get_absolute_url())
        else:
            print form.errors
            return render_to_response(
                "links/submit.html", {
                    "form": form,
                    "active_nav_item": "submit"
                }, context_instance=RequestContext(request))
    else:
        return render_to_response(
            "links/submit.html", {
                "form": SubmitLinkForm(),
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
            print form.errors
            return render_to_response("links/edit.html", {
                    "form": form
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("links/edit.html", {
            "form": EditLinkForm(
                instance=get_object_or_404(
                    Link, pk=pk, posted_by=request.user)),
            }, context_instance=RequestContext(request))


class LinkDetail(DetailView):

    queryset = Link.objects.all()

    def get_object(self):
        object  = super(LinkDetail, self).get_object()
        object.inc_shown()
        return object


def query_builder(request, **kwargs):
    """Builds query via requestitem, if kwargs given overrides request.
    """
    query = Q()

    if kwargs.has_key('user'):
        query = query & Q(posted_by__username=kwargs['user'])
    else:
        if request.GET.has_key("user"):
            query = query & Q(posted_by__username=request.GET['user'])

    if kwargs.has_key("channel"):
        query = query & Q(channel__slug=kwargs['channel'])
    else:
        if request.GET.has_key("channel"):
            query = query & Q(channel__slug=request.GET['channel'])

    if kwargs.has_key("days"):
        query = query & Q(posted_at__gte=datetime.today() - timedelta(days=kwargs['days']))
    else:
        if request.GET.has_key("days"):
            try:
                days = int(request.GET["days"])
            except ValueError:
                days = False

            if days:
                query = query & Q(posted_at__gte=datetime.today() - timedelta(days=days))

    if kwargs.has_key("order_by"):
        order_by = kwargs["order_by"]
    else:
        order_by = request.GET.get("order_by", False)

    if order_by in ("vote_score", "comment_score", "-vote_score",
                    "-comment_score", "posted_at", "-posted_at"):
        return Link.objects_with_scores.filter(query).order_by(order_by)
    else:
        return Link.objects_with_scores.filter(query).order_by("-vote_score")

class LinksListView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):
        return query_builder(self.request)

class HighestLinksView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):
        return query_builder(self.request)

    def get_context_data(self, **kwargs):
        context = super(HighestLinksView, self).get_context_data(**kwargs)
        context['active_nav_item'] = "highest"
        context['top_channels'] = Channel.objects.all().annotate(
            link_count=Count("link")).order_by("-link_count")
        return context

class LinksFromUserView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):
        return query_builder(self.request, user=self.kwargs["user"])

    def get_context_data(self, **kwargs):
        context = super(LinksFromUserView, self).get_context_data(**kwargs)
        if self.request.user.username == self.kwargs["user"]:
            context['active_nav_item'] = "from_me"
        context['top_channels'] = Channel.objects.all().annotate(
            link_count=Count("link")).order_by("-link_count")
        return context

class LinksFromChannelView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):
        return query_builder(self.request, channel=self.kwargs["channel"])

    def get_context_data(self, **kwargs):
        context = super(LinksFromChannelView, self).get_context_data(**kwargs)
        context['top_channels'] = Channel.objects.all().annotate(
            link_count=Count("link")).order_by("-link_count")
        context['active_channel'] = get_object_or_404(
            Channel, slug=self.kwargs["channel"])
        return context

