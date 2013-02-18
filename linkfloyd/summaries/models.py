from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from links.models import Link
from channels.models import Subscription


class Unseen(models.Model):
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)

    def __unicode__(self):
        return "%s unseen by %s" % (self.link, self.user)


@receiver(post_save, sender=Link)
def link_saved(sender, **kwargs):
    if kwargs['created'] == True:
        link = kwargs['instance']
        subscriptions = Subscription.objects.filter(channel=link.channel)
        for subscription in subscriptions:
            Unseen.objects.get_or_create(user=subscription.user, link=link)


@receiver(pre_delete, sender=Link)
def link_deleted(sender, **kwargs):
    link = kwargs['instance']
    Unseen.objects.filter(link=link).delete()
