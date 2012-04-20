from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db.models import Count

from links.models import Link
from links.models import Subscription as LinkSubscription

from django.contrib.auth.models import User

from utils import reduced_markdown

from django.template.loader import render_to_string
from django.conf import settings

from django.core.mail import send_mass_mail

# Create your models here.

class Comment(models.Model):
    link = models.ForeignKey(Link)
    body = models.TextField(help_text="you can use markdown here")
    as_html = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, related_name="posted_by")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s's comment on %s" % (self.posted_by, self.link)

    def save(self, *args, **kwargs):
        from utils import reduced_markdown
        self.as_html = reduced_markdown(self.body, safe_mode="remove")
        super(Comment, self).save(*args, **kwargs)

@receiver(post_save, sender=Comment, dispatch_uid="comment_saved")
def comment_saved(sender, **kwargs):
    if kwargs['created'] == True:

        comment = kwargs['instance']

        # update links updated_at
        comment.link.updated_at = comment.posted_at
        comment.link.comment_score = comment.link.comment_set.all().count()
        comment.link.save()

	# send mail to followers
        recipients = [subscription.user.email for subscription in \
                      LinkSubscription.objects.filter(
                          link=comment.link).exclude(user=comment.posted_by)]
        title = render_to_string(
            "comments/subject.txt",{"comment": comment})
        body = render_to_string(
            "comments/body.txt", {"comment": comment})
        messages = []
        for recipient in recipients:
            messages.append(
                (
                    title,
                    body,
                    "Linkfloyd %s" % settings.DEFAULT_FROM_EMAIL,
                    [recipient,]
                )
            )

        send_mass_mail(messages, fail_silently=False)
        LinkSubscription.objects.get_or_create(
            user=comment.posted_by, link=comment.link)


@receiver(post_delete, sender=Comment, dispatch_uid="comment_deleted")
def comment_saved(sender, **kwargs):
    comment = kwargs['instance']
    comment.link.comment_score = comment.link.comment_set.all().count()
    comment.link.save()

