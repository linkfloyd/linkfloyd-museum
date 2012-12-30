from django.contrib import admin
from notifications.models import Notification
from notifications.models import NotificationPreference
from notifications.models import NotificationType


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('actor', 'type', 'recipient', 'seen')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationPreference)
admin.site.register(NotificationType)
