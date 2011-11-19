from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django.db import models
from django.db.models import F
from django.db.models import Sum

from django_votes.models import VotesField

from taggit.managers import TaggableManager

SITE_RATINGS = (
    ("G", _("Suitable with any audience type.")),
    ("PG",_("Can Contain rude gestures, the lesser swear words, or mild violence")),
    ("R", _("Can Contain such things as harsh profanity, intense violence, nudity or drug use.")),
    ("X", _("Can Contain hardcore sexual imagery or extremely disturbing violence."))
)

SITE_LANGUAGES = (
    ("tr", "Turkish"),
    ("en", "English"),
)

class LinksWithScoresManager(models.Manager):
    def get_query_set(self):
        return super(LinksWithScoresManager, self).get_query_set().filter(\
            is_banned=False).annotate(score=Sum('linkvote__value'))

class Link(models.Model):

    posted_by = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(help_text=_("paste url of your link here"))

    title = models.CharField(max_length=2048, blank=True,
        help_text=_("title of your link"))

    description = models.CharField(max_length=4096, null=True, blank=True,
        help_text=_("say something about that link"))
    thumbnail_url = models.URLField(null=True, blank=True)

    rating = models.CharField(
        max_length=2,
        choices=SITE_RATINGS,
        help_text=_("warn people about your link")
    )

    language = models.CharField(max_length=5, choices=SITE_LANGUAGES)
    votes = VotesField()
    tags = TaggableManager()
    shown = models.PositiveIntegerField(default=0)

    is_banned = models.BooleanField(default=False)

    objects = models.Manager()
    objects_with_scores = LinksWithScoresManager()

    def get_domain(self):
        from urllib2 import urlparse
        return urlparse.urlparse(self.url).hostname

    def get_absolute_url(self):
        return "/links/%s/" % self.id

    def get_full_url(self):
        from django.contrib.sites.models import Site
        return "http://" + Site.objects.get_current().domain + self.get_absolute_url()

    def get_editing_url(self):
        return "/links/edit/%s/" % self.id

    def get_sharing_url(self):
        return "%s?site=%s" % (Site.objects.get_current().domain, self.url)

    def inc_shown(self):
        self.shown = F('shown') + 1
        self.save()

    def __unicode__(self):
        return self.url
