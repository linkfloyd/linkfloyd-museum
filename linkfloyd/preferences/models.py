from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from links.models import SITE_RATINGS
from django.db.utils import DatabaseError

from django.utils.translation import ugettext as _

class UserPreferences(models.Model):
    user = models.ForeignKey(User)
    description= models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("describe yourself"))
    # known_languages = models.ManyToManyField(Language)
    max_rating = models.PositiveIntegerField(
        verbose_name = _("Maximum Rating"),
        choices=SITE_RATINGS,
        help_text=_("how much can you handle?"),
        default=1
    )
    summary_mails = models.CharField(
        max_length=10,
        default="daily",
        choices=(("daily", _("Daily")),
                 ("weekly", _("Weekly")),
                 ("monthly", _("Monthly")),
                 ("never", _("Never Send"))),
        verbose_name=_("Summary Emails"),
        help_text=_("When do you want to get summaries of " \
                    "your subscripted channels")
    )
    def __unicode__(self):
        return "Preferences of %s" % self.user

def create_preferences(sender, instance, created, **kwargs):
    if created and UserPreferences.objects.filter(\
        user__username=instance.username).count() == 0:
        try:
            UserPreferences.objects.create(user=instance, max_rating=1)
        except DatabaseError:
            pass

post_save.connect(create_preferences, sender=User)
