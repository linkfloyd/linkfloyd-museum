from django.contrib import admin
from notifications.models import Notification
from notifications.models import NotificationPreference
from notifications.models import NotificationType


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('actor', 'type', 'recipient', 'seen')


class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'subscription_status')


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'label')


admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationPreference, NotificationPreferenceAdmin)
admin.site.register(NotificationType, NotificationTypeAdmin)
