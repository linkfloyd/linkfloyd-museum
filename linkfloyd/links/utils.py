from django.db.models import Q, Sum

def get_in(d, k, p, df=None):
    if k in d:
        if d[k] in p:
            return d[k]
    return df

def context_builder(request, **kwargs):

    ''' (request object, [kwargs...]) -> response dict
        
    Builds query via request item contents overriden by kwargs.

    links_from and instance properties
    ----------------------------------

    * Request object SHOULD HAVE "links_from" property as string which holds
      type of what we are trying to list. For ex: if "links_from" is "user"
      that means, we're going to list links from user.

    * If "links_from" is "subscriptions", returns links from subscripted
      channels of current user. If current user is not authenticated, returns
      all links.

    * If "links_from" is "user", returns links posted by user. "instance"
      keyword supplied and it must an instance of User model.

    * If "links_from" is "channel", returns links posted to channel.
     "instance" keyword supplied and it must contain an instance of Channel
     model.

    * If "links_from" is "likes", returns links liked by user. "instance"
      keyword supplied and it must contain an instance of User model.

    * Request object can have "days" property which is integer, that limits
      query in time. 

    ordering and limiting
    ---------------------

    * Request object can be supplied with "days" property which is positive
      integer to limit links in time.

    * Request object can be supplied with "ordering" property which is 
      string that can contain "contreversial", "top" or "latest" to get
      links in that way.

    '''
    from links.models import Link
    from preferences.models import UserPreferences
    from channels.models import Subscription
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
        # TODO: this line can be optimised:
        query = query & Q(channel_id__in=[subscription.channel for \
            subscription in Subscription.objects.filter(user=request.user).select_related("channel")])
    elif response['links_from'] == "channel":
        query = query & Q(channel=response['instance'])
    elif response['links_from'] == "user":
        query = query & Q(posted_by=response['instance'])
    elif response['links_from'] == "likes":
        # TODO: this line can be optimised:
        vote_model = get_vote_model('links.LinkVote')
        votes = vote_model.objects.filter(voter=response['instance'], value=1
            ).select_related("object")
        query = query & Q(id__in = [vote.object.id for vote in votes])

    if response['days']:
        query = query & Q(
            posted_at__gte=datetime.today() - timedelta(days=response['days']))

    links = Link.objects.filter(query)

    if user_is_authenticated:

        # Filter links that not in known languages and rating higer than users.
        preferences = UserPreferences.objects.get(user=request.user)
        query = query & Q(rating__lte  = preferences.max_rating)
        links = links.extra(select={
            'is_owned':      'posted_by_id=%s' % request.user.id,

            'is_subscribed': 'SELECT COUNT(*) FROM links_subscription WHERE '
                             'user_id=%s '
                             'AND '
                             'id=links_subscription.link_id' % request.user.id,

            'is_voted_up':   'SELECT COUNT(*) FROM links_linkvote WHERE '
                             'voter_id=%s '
                             'AND '
                             'object_id=links_link.id '
                             'AND '
                             'value=1' % request.user.id,

            'is_voted_down': 'SELECT COUNT(*) FROM links_linkvote WHERE '
                             'voter_id=%s '
                             'AND '
                             'object_id=links_link.id '
                             'AND '
                             'value=-1' % request.user.id})

    links = links.select_related("posted_by", "channel").order_by({
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
