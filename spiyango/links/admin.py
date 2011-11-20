from django.contrib import admin
from spiyango.links.models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'posted_at', 'rating', 'shown', 'language')
admin.site.register(Link, LinkAdmin)
# admin.site.register(Link.vote_model)

