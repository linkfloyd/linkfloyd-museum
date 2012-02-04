from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from channels.forms import CreateChannelForm
from channels.models import Subscription, Channel
from django.contrib import messages


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
            messages.add_message(request, messages.INFO, 'You Created %s Channel')
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
def subscribe(request, slug):
    channel = get_object_or_404(Channel, slug=slug)

    try:
        subscription = Subscription.objects.create(user=request.user, channel=channel)
    except Subscription.IntegrityError:
        messages.add_message(request, messages.INFO, 'You are already subscribed to %s channel' % channel)
        return HttpResponseRedirect(channel.get_absolute_url())

    messages.add_message(request, messages.INFO, 'You are subscribed to %s channel' % channel)
    return HttpResponseRedirect(channel.get_absolute_url())

@login_required
def unsubscribe(request, slug):
    channel = get_object_or_404(Channel, slug=slug)

    try:
        subscription = Subscription.objects.get(user=request.user, channel=channel)
    except Subscription.DoesNotExist:
        messages.add_message(request, messages.INFO, 'You are already unsubscribed from %s channel' % channel)
        return HttpResponseRedirect(channel.get_absolute_url())
    except Subscription.MultipleObjectsReturned:
        Subscription.objects.filter(user=request.user, channel=channel).delete()
        messages.add_message(request, messages.INFO, 'You are unsubscribed to %s channel' % channel)
        return HttpResponseRedirect(channel.get_absolute_url())

    subscription.delete()
    messages.add_message(request, messages.INFO, 'You are unsubscribed to %s channel' % channel)
    return HttpResponseRedirect(channel.get_absolute_url())
