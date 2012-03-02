from django.db.models import Q, Sum

def query_builder(request, **kwargs):
    """Builds query via requestitem, if kwargs given overrides request.
    """
    from links.models import Link, Report, Channel
    from preferences.models import UserPreferences
    from channels.models import Channel, Subscription
    from datetime import datetime
    from datetime import timedelta

    query = Q()

    if request.user.is_authenticated():

        query = query & ~Q(report__in =\
        Report.objects.filter(reporter=request.user))

        preferences = UserPreferences.objects.get(user=request.user)

        query = query &\
                Q(language__in = preferences.known_languages.all()) &\
                Q(rating__lte  = preferences.max_rating)

        if kwargs.has_key('from_subscriptions'):
            query = query & Q(channel__in=[\
            subscription.channel for subscription in\
            Subscription.objects.filter(user=request.user)
            ])

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

    if kwargs.has_key("domain"):
        query = query & Q(url__contains=kwargs['domain'])
    else:
        if request.GET.has_key("domain"):
            query = query & Q(url__contains=request.GET['domain'])

    if kwargs.has_key("days"):
        query = query & Q(
            posted_at__gte=datetime.today() - timedelta(days=kwargs['days']))
    else:
        if request.GET.has_key("days"):
            try:
                days = int(request.GET["days"])
            except ValueError:
                days = False

            if days:
                query = query & Q(
                    posted_at__gte=datetime.today() - timedelta(days=days))

    if kwargs.has_key("order_by"):
        order_by = kwargs["order_by"]
    else:
        order_by = request.GET.get("order_by", False)

    if order_by in ("vote_score", "comment_score", "-vote_score",
                    "-comment_score", "posted_at", "-posted_at"):
        return Link.objects_with_scores.filter(query).order_by(order_by)
    else:
        return Link.objects_with_scores.filter(query).order_by("-posted_at")
