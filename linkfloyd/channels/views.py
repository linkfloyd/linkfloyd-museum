from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from channels.forms import CreateChannelForm, UpdateChannelForm
from channels.models import Subscription, Channel
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Count
from django.utils.translation import ugettext as _

@login_required
def create(request):
    if request.POST:
        form = CreateChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            Subscription.objects.create(
                user=request.user,
                channel=channel,
                status="admin",
                email_frequency="weekly"
            )
            messages.add_message(
                request,
                messages.INFO,
	        	'You Created %s Channel' % channel
            )
            return HttpResponseRedirect(channel.get_absolute_url())
        else:
            return render_to_response(
                "channels/create.html", {
                    "form": form
                }, context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
            "channels/create.html", {
                "form": CreateChannelForm()
            }, context_instance=RequestContext(request)
        )

@login_required
def update(request, slug):
    if request.POST:
        channel = get_object_or_404(Channel, slug=slug)
        
        get_object_or_404(
            Subscription,
            user=request.user,
            channel=channel,
            status="admin"
        )

        form = UpdateChannelForm(request.POST,instance=channel)
        if form.is_valid():
            channel = form.save()
            messages.add_message(
                request,
                messages.INFO,
                _('You Updated %s Channel' % channel)
            )
            return HttpResponseRedirect(channel.get_absolute_url())
        else:
            return render_to_response(
                "channels/update.html", {
                    "form": form
                }, context_instance=RequestContext(request))
    else:
        channel = get_object_or_404(Channel, slug=slug)
        get_object_or_404(
            Subscription,
            user=request.user,
            channel=channel,
            status="admin"
        )
        return render_to_response(
           "channels/update.html", {
                "form": UpdateChannelForm(instance=channel)
            }, context_instance=RequestContext(request)
        )


class BrowseChannelsView(ListView):
    context_object_name = "channels"
    paginate_by = 20
    template_name = "channels/channel_list.html"

    def get_queryset(self):
        return Channel.objects.filter(parent=None).annotate(
	    num_of_subscribers=Count("subscription")).order_by(
            "-is_official", "-num_of_subscribers")

    def get_context_data(self, **kwargs):
        context = super(BrowseChannelsView, self).get_context_data(**kwargs)
        context['active_nav_item'] = "channels"
        context['title'] = _("Browsing Channels")
        return context

class SubscriptionsView(BrowseChannelsView):
    def get_queryset(self):
        return Channel.objects.filter(
            id__in=[s.channel.id for s in Subscription.objects.filter(user=self.request.user)])

    def get_context_data(self, **kwargs):
        context = super(SubscriptionsView, self).get_context_data(**kwargs)
        context['active_nav_item'] = "channels"
        context['title'] = _("Browsing Your Subscripted Channels")
        return context
