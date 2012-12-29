from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext

from utils import get_info

from channels.models import Channel
from links.models import Link

from channels.models import Subscription as ChannelSubscription
from links.models import Subscription as LinkSubscription

from comments.models import Comment
from comments.forms import CommentForm

from django.utils.translation import ugettext as _

def fetch_info(request):
    if "url" in request.GET:
        info = get_info(request.GET['url'])
        if not info:
            return HttpResponse(status=404)
        dummy_link = {
            "url": info['url'],
            "thumbnail_url": info.get("image"),
            "title": info.get("title"),
            "description": info.get("description"),
            "player": info.get("player")
        }
        return HttpResponse(
            simplejson.dumps({
                "html": render_to_string(
                    "links/attachment.html",
                    {
                        "link": dummy_link,
                        "attachment_editable": True
                    }
                ),
                "info": info
            }), 'application/javascript'
        )
    else:
        return HttpResponse(status=400)


@login_required
def delete_link(request):
    if "id" in request.GET:
        try:
            link = Link.objects.get(
                pk=request.GET['id'], posted_by=request.user)
        except Link.DoesNotExist:
            return HttpResponse(status=404)
        link.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@login_required
def delete_comment(request):
    if "id" in request.GET:
        try:
            comment = Comment.objects.get(
                pk=request.GET['id'], posted_by=request.user)
        except Comment.DoesNotExist:
            return HttpResponse(status=404)
        comment.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@login_required
def get_update_comment_form(request):
    if "id" in request.GET:
        try:
            comment = Comment.objects.get(
                pk=request.GET['id'], posted_by=request.user)
        except Comment.DoesNotExist:
            return HttpResponse(status=404)
        return render_to_response("links/update_comment_form.html", {
            "form": CommentForm(instance=comment)
            }, context_instance=RequestContext(request))
    else:
        return HttpResponse(status=400)

def switch_channel_subscription(request):
    """
    Workflow:
    * User submits subscription request:

        Status 1:
          - request.POST does not have "requested_status":
          - user is not subscribed to channel.
        Response:
          user subscribes channel as "subscriber"

        Status 2:
          - request.POST has "requested_status" as "admin"
          - there is no admin of channel
          - request.POST has no sure = True
        Response:     
          Api rejects request with, "ask_for_sure" parameter.
          Client, pops up a window that confirms that user is 
          sure, and makes post request again with sure = True.

        Status 3:
          - same with status 2 but request.POST has sure = True
        Response:
          User becomes admin of channel.

        Status 4:
          - User is subscribed to channel
          - User is not admin or moderator of channel
        Response:
          User unsubscribes from channel.

       Status 5:
         - User is admin or moderator of channel
         - request.POST has no sure = True
       Response:
         Api rejects request with, "ask_for_sure" parameter.
         Client pops up a window that confirms that user
         wants to unsubscribe from channel. If confirmed, it
         makes same post again with sure = True.

        Status 6:
          - User is admin or moderator of channel
          - request.POST has sure = True
        Response:
          User unsubscribes from channel.
    """

    if not request.user.is_authenticated():
        return HttpResponse(simplejson.dumps(
            {"notification_text": _("You have to be logged in to "
                                    "complete this action.")}
        ), status=401)

    if not "channel_slug" in request.POST:
        return HttpResponse(status=404)

    try:
        channel = Channel.objects.get(slug=request.POST["channel_slug"])
    except Channel.DoesNotExist:
        return HttpResponse(status=404)
 
    try:
        subscription = ChannelSubscription.objects.get(
            user=request.user,
            channel=channel
        )
    except ChannelSubscription.DoesNotExist:
        subscription = None
    
    # Status 1
    if not subscription:
        
        if  not "requested_status" in request.POST:
            subscription = ChannelSubscription.objects.create(
                channel=channel,
                user=request.user,
                status="subscriber"
            )
            return HttpResponse(simplejson.dumps({
                    "status": "subscribed",
                    "update_text": _("Unsubscribe"),
            }), status = 200)
        
        if  request.POST.get("requested_status") == "admin":
            if request.POST.get("sure") == True:
                subscription = ChannelSubscription.objects.create(
                    channel=channel,
                    user=request.user,
                    status="admin"
                )
            else:
                return HttpResponse(simplejson.dumps({
                    "status": "confirmation_needed",
                    "confirmation_text": _(
						"Are you sure that you want to be " \
                        "admin of this channel?")
                }))

        return HttpResponse(status=400)

    else: # if user subscribed to channel
        if  subscription.status == "admin" or \
            subscription.status == "moderator":
            if  request.POST.get("sure") == "true":
                subscription.delete()
                return HttpResponse(simplejson.dumps({
                    "status": "unsubscribed",
                    "update_text": _("Subscribe")
                }))
            else:
                return HttpResponse(simplejson.dumps({
                    "status": "confirmation_needed",
                    "confirmation_text": _("You will loose your " \
                                           "adminstration rights from this " \
                                           "channel. Are you sure?")
                }))
        else:
            subscription.delete()
            return HttpResponse(simplejson.dumps({
                "status": "unsubscribed",
                "update_text": _("Subscribe")
            }))


@login_required
def switch_link_subscription(request):
    if "link_id" in request.POST:
        # try to get link, or return 404
        try:
            link = Link.objects.get(id=request.POST['link_id'])
        except Link.DoesNotExist:
            return HttpResponse(status=404)

        # subscription = from database or false
        try:
            subscription = LinkSubscription.objects.get(
                user=request.user, link=link)
        except:
            subscription = False

        if subscription:
            if subscription.status == 0:
                subscription.status = 1
                subscription.save()
                return HttpResponse(
                    simplejson.dumps({
                        "status": "subscribed",
                        "update_text": "Unsubscribe",
                        "update_title": "Do not email me when somebody" \
                                        "comments on that link"
                    }, 'application/javascript')
                )
            elif subscription.status == 1:
                subscription.status = 0
                subscription.save()
                return HttpResponse(
                    simplejson.dumps({
                        "status": "unsubscribed",
                        "update_text": "Subscribe",
                        "update_title": "Email me when somebody comments " \
                                        "on that link"
                    }, 'application/javascript')
                )
        else:
            LinkSubscription.objects.create(
                user=request.user,
                link=link,
                status=1
            )
            return HttpResponse(
                simplejson.dumps({
                    "status": "subscribed",
                    "update_text": "Unsubscribe",
                    "update_title": "Do not email me when somebody " \
                                    "comments on that link"
                }, 'application/javascript')
            )
    else:
        return HttpResponse(status=400)


def channels_list(request):

    query_string = request.GET.get("q", False)
    if query_string:
        channels = Channel.objects.filter(name__contains=query_string)
    else:
        channels = Channel.objects.all()
    response = []
    for c in channels:
        response.append({"id": c.id, "name": c.name})

    return HttpResponse(
        simplejson.dumps(response, 'application/javascript')
    )

