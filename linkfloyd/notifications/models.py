from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


class NotificationType(models.Model):
    label = models.SlugField(max_length=32)
    name = models.CharField(max_length=255)
    is_important = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class NotificationPreferenceManager(models.Manager):
    def get(self, user, type):
        ''' (User, ActivityType) -> NotificationPreference

        Returns NotificationPreference for given userand activity type.
        If does not exists, creates it.
        '''
        try:
            obj = super(NotificationPreferenceManager, self).get(
                user=user, notification_type=type)
        except ObjectDoesNotExist:
            obj = self.create(user=user, notification_type=type,
                subscription_status=1 if type.label in (
                    "commented_your_post", "upvoted_your_post") else 0)
        return obj


class NotificationPreference(models.Model):
    user = models.ForeignKey(User)
    notification_type = models.ForeignKey(NotificationType)
    subscription_status = models.PositiveIntegerField(choices=(
        (0, "Only show on site"),
        (1, "Send me email")), default=0)
    objects = NotificationPreferenceManager()

    def __unicode__(self):
        return '%s\'s setting on %s notifications' % (self.user,
            self.notification_type)


class Notification(models.Model):

    actor = models.ForeignKey(User, related_name='actor', null=True,
        blank=True)
    recipient = models.ForeignKey(User, related_name='recipient', null=True,
        blank=True)
    target_object_ctype = models.ForeignKey(ContentType,
        blank=True, null=True)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target_object = GenericForeignKey('target_object_ctype',
        'target_object_id')
    type = models.ForeignKey(NotificationType)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    custom_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "notifications"

    def __unicode__(self):
        return "'%s' notification for %s" % (self.type, self.recipient)


@receiver(post_save, sender=Notification, dispatch_uid="notification_saved")
def notification_saved(sender, **kwargs):
    notification = kwargs['instance']

    preference = NotificationPreference.objects.get(notification.recipient,
        notification.type)

    if preference.subscription_status == 1:

        # send mail to followers
        title = render_to_string(
            "notifications/%s/email_subject.txt" % notification.type.label,
            {"notification": notification})
        body = render_to_string(
            "notifications/%s/email_body.txt" % notification.type.label,
            {"notification": notification})

        send_mail(title, body, settings.DEFAULT_FROM_EMAIL,
            [notification.recipient.email, ])
