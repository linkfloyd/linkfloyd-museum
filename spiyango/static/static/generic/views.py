from django.shortcuts import render_to_response
from links.models import Link

def index(request):
    return render_to_response("index.html", {"todays_links": Link.objects.all()})
