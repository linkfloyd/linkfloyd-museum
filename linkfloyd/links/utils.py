from django.db.models import Q, Sum

def get_in(d, k, p, df=None):
    if k in d:
        if d[k] in p:
            return d[k]
    return df

def context_builder(request, **kwargs):
    """Builds query via requestitem, if kwargs given overrides request.
    """
    from links.models import Link, Report, Channel
    from preferences.models import UserPreferences
    from channels.models import Channel, Subscription
    from datetime import datetime
    from datetime import timedelta
    from django.core.paginator import Paginator
    from django.core.paginator import EmptyPage
    from django.core.paginator import PageNotAnInteger
    from django.utils.translation import ugettext as _
    from qhonuskan_votes.utils import get_vote_model

    response = {
        "links_from": kwargs.get("links_from"),
        "instance": kwargs.get("instance"),
        "days": kwargs.get("days"),
        "ordering": get_in(
            request.GET, "ordering", [
                "controversial", "top", "latest"], "hot"),
    }
    if 'highlight' in request.GET:
        try:
            response['highlight'] = int(request.GET['highlight'])
        except ValueError:
            pass

    response['title'] = {
        "subscriptions": _("Posts From Your Subscripted Channels"),
        "user": _("Posts From %s") % response['instance'],
        "channel": _("Posts From %s Channel") % response['instance'],
        "likes": _("Posts liked by %s") % response['instance'],
    }.get(response['links_from'], _("All Posts Shared on Linkfloyd"))

    # is_authenticated method hits db on every call, so i cached it with this.
    user_is_authenticated = request.user.is_authenticated()

    query = Q()
    if response['links_from'] == "subscriptions" and user_is_authenticated:
        query = query & Q(channel__in=[subscription.channel for \
            subscription in Subscription.objects.filter(user=request.user)])
    elif response['links_from'] == "channel":
        query = query & Q(channel=response['instance'])
    elif response['links_from'] == "user":
        query = query & Q(posted_by=response['instance'])
    elif response['links_from'] == "likes":
        vote_model = get_vote_model('links.LinkVote')
        votes = vote_model.objects.filter(voter=request.user, value=1)
        query = query & Q(id__in = [vote.object.id for vote in votes])

    if response['days']:
        query = query & Q(
            posted_at__gte=datetime.today() - timedelta(days=response['days']))

    if user_is_authenticated:

        query = query & ~Q(report__in =\
            Report.objects.filter(reporter=request.user))

        # Filter links that not in known languages and rating higer than users.
        preferences = UserPreferences.objects.get(user=request.user)
        query = query & \
                Q(rating__lte  = preferences.max_rating)

    links = Link.objects.filter(query).order_by({
    "hot": "-updated_at",
        "controversial": "-comment_score",
        "top": "-vote_score",
        "latest": "-posted_at",
    }[response['ordering']])

    paginator = Paginator(links, 25)

    page = request.GET.get('page', 1)

    try:
        response['links'] = paginator.page(page)
    except PageNotAnInteger:
        response['links'] = paginator.page(1)
    except EmptyPage:
        response['links'] = paginator.page(paginator.num_pages)

    return response
