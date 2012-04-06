from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Channel(models.Model):
    """Channel model for linkfloyd.

    Users can be members or admins of channels. If an user is admin of channel
    """

    name = models.CharField(verbose_name=_("title"), max_length=255, unique=True)
    slug = models.SlugField(verbose_name=_("slug"), max_length=255, unique=True)
    description = models.TextField(verbose_name=_("description"))
    is_official = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/links/channel/%s/" % self.slug

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name="channel_subscriptions")
    channel = models.ForeignKey(Channel)

    status = models.CharField(
        max_length=12,
        default="member",
        choices=(("member", "Member"),
                 ("admin", "Admin")))

    email_frequency = models.CharField(
        max_length=12,
        default="daily",
        choices=(("daily", "daily"),
                 ("weekly", "Weekly"),
                 ("noemail", "No Email")))

    def __unicode__(self):
        return u"%s's subscription to %s as %s" % (
            self.user, self.channel, self.status)

    class Meta:
        unique_together = ("user", "channel")
