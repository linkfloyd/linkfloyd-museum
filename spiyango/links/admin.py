from django.contrib import admin
from spiyango.links.models import Link
from spiyango.links.models import Channel
from spiyango.links.models import Comment
from spiyango.links.models import Report

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'posted_at', 'rating', 'shown', 'language')
admin.site.register(Link, LinkAdmin)
admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Report)

