from django.shortcuts import render_to_response
from links.models import Link
from django.db.models import Sum
from django.template import RequestContext

def index(request):
    return render_to_response(
        "index.html", {
            "latest_links": Link.objects.all().order_by("-posted_at").annotate(\
                score=Sum('linkvote__value'))[:5],
            "top_links": Link.objects.all().order_by("-posted_at").annotate(\
                score=Sum('linkvote__value')).order_by("-score")[:5]
        },
        context_instance=RequestContext(request))
