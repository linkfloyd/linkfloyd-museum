from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Language(models.Model):
    code = models.CharField(
        max_length=5,
        null=True
    )
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class Channel(models.Model):
    """Channel model for linkfloyd.

    Users can be members or admins of channels.
    """

    name = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=255,
        unique=True
    )
    description = models.CharField(
        max_length="255",
        verbose_name=_("description"),
        help_text=_("describe this channel in 255 chars")
    )
    notes = models.TextField(
        help_text=_("notes and rules about that channel"),
        blank = True,
        null = True
    )
    language = models.ForeignKey(
        Language,
        help_text=_("which language do you expect to be spoken "\
                    "in that channel")
    )

    is_official = models.BooleanField(default=False)

    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent channel"),
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/links/channel/%s/" % self.slug

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name="channel_subscriptions"
    )
    channel = models.ForeignKey(Channel)

    status = models.CharField(
        max_length=12,
        default="member",
        choices=(        
            ("admin", _("Admin")),
            ("moderator", _("Moderator")),
            ("subscriber", _("Subscriber"))
        )
    )
    email_frequency = models.CharField(
        max_length=12,
        default="daily",
        choices=(
            ("daily", "daily"),
            ("weekly", "Weekly"),
            ("noemail", "No Email")
        )
    )

    def __unicode__(self):
        return u"%s's subscription to %s as %s" % (
            self.user, self.channel, self.status)

    class Meta:
        unique_together = ("user", "channel")
