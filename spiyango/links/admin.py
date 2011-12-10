from django.contrib import admin
from spiyango.links.models import Link
from spiyango.links.models import Channel
from spiyango.links.models import Comment
from spiyango.links.models import Report

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'posted_at', 'rating', 'shown', 'language')

def mark_as_seen(modeladmin, request, queryset):
    queryset.update(seen=True)

mark_as_seen.short_description = "Mark selected reports as seen"

class ReportAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "reported_link", "note", "seen")
    order_by = ("seen",)
    actions = [mark_as_seen,]

    def reported_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.link.get_absolute_url(), obj.link)

    reported_link.allow_tags = True

admin.site.register(Link, LinkAdmin)
admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Report, ReportAdmin)

