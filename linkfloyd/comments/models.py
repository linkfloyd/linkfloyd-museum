from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from links.models import Link
from links.models import Subscription as LinkSubscription

from django.contrib.auth.models import User

from utils import reduced_markdown

from django.utils.translation import ugettext as _
from datetime import datetime

from notifications.models import Notification, NotificationType
# Create your models here.


class Comment(models.Model):
    link = models.ForeignKey(Link)
    body = models.TextField(
        verbose_name=_("Comment"),
        help_text=_("you can use markdown here"))
    as_html = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, related_name="posted_by")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s's comment on %s" % (self.posted_by, self.link)

    def save(self, *args, **kwargs):
        self.as_html = reduced_markdown(self.body, safe_mode="remove")
        super(Comment, self).save(*args, **kwargs)


@receiver(post_save, sender=Comment, dispatch_uid="comment_saved")
def comment_saved(sender, **kwargs):
    if kwargs['created']:

        comment = kwargs['instance']
        comment.link.comment_score = comment.link.comment_set.all().count()
        comment.link.save()

        for subscription in LinkSubscription.objects.filter(
            link=comment.link).exclude(user=comment.posted_by):

            commented_post = \
                NotificationType.objects.get(label="commented_post")

            commented_your_post = NotificationType.objects.get(
                label="commented_your_post")

            Notification.objects.create(
                actor=comment.posted_by,
                recipient=subscription.user,
                target_object=comment.link,
                type=commented_your_post if comment.posted_by ==
                    subscription.user else commented_post)

        # create subscription
        subscription, created = LinkSubscription.objects.get_or_create(
            user=comment.posted_by, link=comment.link)

        if created:
            subscription.status = 1
            subscription.save()

        # update link's updated at

        comment.link.updated_at = datetime.now()
        comment.link.save()


@receiver(post_delete, sender=Comment, dispatch_uid="comment_deleted")
def comment_deleted(sender, **kwargs):
    comment = kwargs['instance']
    try:
        link = comment.link
    except Link.DoesNotExist:
        link = False

    if link:
        comment.link.comment_score = comment.link.comment_set.all().count()
        comment.link.save()
