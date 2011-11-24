# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Sum, Count
from datetime import datetime
from taggit.models import Tag

from spiyango.links.models import Link
from spiyango.links.forms import SubmitLinkForm, EditLinkForm

from django.db.models import Q

@login_required
def submit(request):
    if request.POST:
        form = SubmitLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.posted_by = request.user
            link.save()
            form.save_m2m()
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

class TopLinksView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):

        try:
            date_id = self.args[0]
        except IndexError:
            date_id = False

        if date_id == "day":
            get_links_after = datetime.today()
        elif date_id == "month":
            get_links_after = datetime.today() + relativedelta(months=1)
        elif date_id == "year":
            get_links_after = datetime.today() + relativedelta(months=12)
        elif date_id == "bigbang":
            get_links_after = False
        else:
            get_links_after = False

        if get_links_after:
            queryset = Link.objects_with_scores.filter(\
                posted_at__lte=get_links_after).order_by("-vote_score")
        else:
            queryset = Link.objects_with_scores.all().order_by("-vote_score")

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TopLinksView, self).get_context_data(**kwargs)
        context['active_nav_item'] = 'highest'
        context['top_tags'] = Tag.objects.annotate(score=Count('taggit_taggeditem_items')).order_by('-score')
        return context

class LatestLinksView(ListView):

    context_object_name = "links"
    queryset = Link.objects_with_scores.all().order_by("-posted_at")
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(LatestLinksView, self).get_context_data(**kwargs)
        context['active_nav_item'] = 'latest'
        return context

class LinksFromUserView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):
        return Link.objects_with_scores.filter(posted_by__username__exact=self.kwargs['username']).order_by("-posted_at")

    def get_context_data(self, **kwargs):
        context = super(LinksFromUserView, self).get_context_data(**kwargs)
        if self.request.user.username == self.kwargs['username']:
            context['active_nav_item'] = 'from_me'
        return context

class LinksListView(ListView):

    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):

        query = Q()

        if self.request.GET.has_key("from"):
            query = query & Q(posted_by__username=self.request.GET['from'])

        if self.request.GET.has_key("tagged"):
            print self.request.GET.getlist('tagged')
            query = query & Q(tags__slug__in=self.request.GET.getlist('tagged'))

        order_by = self.request.GET.get("order_by", False)

        if order_by in ("vote_score", "comment_score", "-vote_score",
                        "-comment_score", "posted_at", "-posted_at"):
            return Link.objects_with_scores.filter(query).order_by(order_by)
        else:
            return Link.objects_with_scores.filter(query)
