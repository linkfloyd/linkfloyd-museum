from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from channels.forms import CreateChannelForm
from channels.models import Subscription
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
            messages.add_message(request, messages.INFO, 'Hello world.')
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




