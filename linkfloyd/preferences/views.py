from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from preferences.forms import UpdatePreferencesForm
from preferences.models import UserPreferences
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _


@login_required
def update(request):
    if request.POST:
        form = UpdatePreferencesForm(request.POST,
            instance = get_object_or_404(
            UserPreferences, user=request.user))
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _('You successfuly updated your preferences.')
            )
            return HttpResponseRedirect("/")
        else:
            return render_to_response("preferences/update.html", {
                "form": form
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("preferences/update.html", {
            "form": UpdatePreferencesForm(instance=
                get_object_or_404(
                    UserPreferences, user=request.user))
        }, context_instance=RequestContext(request))

