from django.contrib import admin
from links.models import Link
from links.models import Subscription
import datetime

def mark_as_seen(modeladmin, request, queryset):
    queryset.update(seen=True)

def mark_as_updated_now(modeladmin, request, queryset):
    queryset.update(updated_at=datetime.datetime.now())

mark_as_seen.short_description = "Mark selected reports as seen"
mark_as_updated_now.short_description = "Mark selected links updated at now"

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'posted_at', 'rating',
                    'shown', 'vote_score')
    actions = [mark_as_updated_now,]

class LinkSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('link', 'user', 'status')

admin.site.register(Link, LinkAdmin)
admin.site.register(Subscription, LinkSubscriptionAdmin)
