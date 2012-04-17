from django.contrib import admin

from channels.models import Channel, Subscription

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'is_official')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'status', 'email_frequency')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Subscription, SubscriptionAdmin)