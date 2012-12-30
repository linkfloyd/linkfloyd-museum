from django.db import models
from django.contrib.auth.models import User
from links.models import SITE_RATINGS
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist


class UserPreferencesManager(models.Manager):
    def get(self, user):
        ''' (User) -> UserPreferences

        Returns UserPreferences for given user.
        If does not exists, creates it.
        '''
        try:
            obj = super(UserPreferencesManager, self).get(user=user)
        except ObjectDoesNotExist:
            obj = self.create(user=user)
        return obj


class UserPreferences(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("describe yourself"))
    max_rating = models.PositiveIntegerField(
        verbose_name=_("Maximum Rating"),
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
        help_text=_("When do you want to get summaries of "
                    "your subscripted channels")
    )
    objects = UserPreferencesManager()

    def __unicode__(self):
        return "Preferences of %s" % self.user
