from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from channels.forms import CreateChannelForm, UpdateChannelForm
from channels.models import Subscription, Channel
from django.contrib import messages
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count

@login_required
def create(request):
    if request.POST:
        form = CreateChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            subscription = Subscription.objects.create(
                user=request.user,
                channel=channel,
                status="admin",
                email_frequency="weekly")
            messages.add_message(
                request,
                messages.INFO,
		'You Created %s Channel' % channel)
            return HttpResponseRedirect(channel.get_absolute_url())
        else:
            return render_to_response(
                "channels/create.html", {
                    "form": form
                }, context_instance=RequestContext(request))
    else:
        return render_to_response(
            "channels/create.html", {
                "form": CreateChannelForm()
            }, context_instance=RequestContext(request))

@login_required
def update(request, slug):
    if request.POST:
        channel = get_object_or_404(Channel, slug=slug)
        subscription = get_object_or_404(
            Subscription, user=request.user, channel=channel, status="admin")
        form = UpdateChannelForm(request.POST,instance=channel)
        if form.is_valid():
            channel = form.save()
            messages.add_message(
                request,
                messages.INFO,
                'You Updated %s Channel' % channel)
            return HttpResponseRedirect(channel.get_absolute_url())
        else:
            return render_to_response(
                "channels/update.html", {
                    "form": form
                }, context_instance=RequestContext(request))
    else:
        channel = get_object_or_404(Channel, slug=slug)
        return render_to_response(
            "channels/update.html", {
                "form": UpdateChannelForm(instance=channel)
            }, context_instance=RequestContext(request))

@login_required
@csrf_protect
def update_subscription(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    action = request.POST.get("action", False)

    if not update:
        return HttpResponseRedirect(channel.get_absolute_url())

    if action == "subscribe":
        try:
            subscription = Subscription.objects.create(
                user=request.user, channel=channel)
        except Subscription.IntegrityError:
            messages.add_message(request, messages.INFO,
                'You are already subscribed to %s channel' % channel)
            return HttpResponseRedirect(channel.get_absolute_url())

        messages.add_message(request, messages.INFO,
        'You are subscribed to %s channel' % channel)
        return HttpResponseRedirect(channel.get_absolute_url())
    elif action == "unsubscribe":
        try:
            subscription = Subscription.objects.get(
                user=request.user, channel=channel)
        except Subscription.DoesNotExist:
            messages.add_message(request, messages.INFO,
                'You are already unsubscribed from %s channel' % channel)
            return HttpResponseRedirect(channel.get_absolute_url())
        except Subscription.MultipleObjectsReturned:
            Subscription.objects.filter(
                user=request.user, channel=channel).delete()
            return HttpResponseRedirect(channel.get_absolute_url())
        subscription.delete()
        messages.add_message(request, messages.INFO,
            'You are unsubscribed to %s channel' % channel)
        return HttpResponseRedirect(channel.get_absolute_url())
    else:
        return HttpResponseRedirect(channel.get_absolute_url())


class BrowseChannelsView(ListView):
    context_object_name = "channels"
    paginate_by = 20
    template_name = "channels/channel_list.html"

    def get_queryset(self):
        return Channel.objects.annotate(
	    num_of_subscribers=Count("subscription")).order_by(
                "-is_official", "-num_of_subscribers")

    def get_context_data(self, **kwargs):
        context = super(BrowseChannelsView, self).get_context_data(**kwargs)
        context['active_nav_item'] = "channels"
        context['title'] = "Browsing Channels"
        return context

class SubscriptionsView(BrowseChannelsView):
    def get_queryset(self):
        return Channel.objects.filter(
            id__in=[s.channel.id for s in Subscription.objects.filter(user=self.request.user)])

    def get_context_data(self, **kwargs):
        context = super(SubscriptionsView, self).get_context_data(**kwargs)
        context['active_nav_item'] = "channels"
        context['title'] = "Browsing Your Subscripted Channels"
        return context
