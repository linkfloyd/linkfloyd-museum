from tastypie.resources import ModelResource
from links.models import Link

class LinkResource(ModelResource):
    class Meta:
        queryset = Link.objects.all()
