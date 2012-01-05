from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from links.models import Language
from links.models import SITE_RATINGS

class UserPreferences(models.Model):
    user = models.ForeignKey(User)
    known_languages = models.ManyToManyField(Language)
    max_rating = models.PositiveIntegerField(
        verbose_name = "Maximum Rating",
        choices=SITE_RATINGS,
        help_text="how much can you handle?"
    )
    def __unicode__(self):
        return "Preferences of %s" % self.user


def create_preferences(sender, instance, created, **kwargs):
    if created:
        UserPreferences.objects.create(user=instance)

post_save.connect(create_preferences, sender=User)