from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django.db import models
from django.db.models import F
from django.db.models import Sum

from spiyango.utils import SumWithDefault
from spiyango.channels.models import Channel

from qhonuskan_votes.models import VotesField

from taggit.managers import TaggableManager

from transmeta import TransMeta


SITE_RATINGS = (
    (1, _("Safe Posts (only safe content)")),
    (2, _("Moderate (can contain nudity, rude gestures)")),
    (3, _("Liberal (hell yeah.)")),
)

SITE_LANGUAGES = (
    ("tr", "Turkish"),
    ("en", "English"),
)

class Comment(models.Model):
    link = models.ForeignKey("Link")
    body = models.TextField()
    posted_by = models.ForeignKey(User, related_name="posted_by")
    posted_at = models.DateTimeField(auto_now_add=True)
    reported_by = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return "%s's comment on %s" % (self.posted_by, self.link)


class Language(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class LinksWithScoresManager(models.Manager):
    def get_query_set(self):
        return super(LinksWithScoresManager, self).get_query_set().filter(\
            is_banned=False).annotate(
                vote_score=SumWithDefault('linkvote__value', default=0))

class Link(models.Model):
    posted_by = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(help_text=_("paste url of your link here"))

    title = models.CharField(max_length=2048, blank=True,
        help_text=_("title of your link"))

    description = models.CharField(max_length=4096, null=True, blank=True,
        help_text=_("say something about that link"))

    thumbnail_url = models.URLField(null=True, blank=True)

    rating = models.PositiveIntegerField(
        choices=SITE_RATINGS,
        help_text=_("warn people about your link")
    )

    language = models.ForeignKey(Language)
    votes = VotesField()

    shown = models.PositiveIntegerField(default=0)
    player = models.TextField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)

    channel = models.ForeignKey(Channel)

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
        return "%s by %s" % (self.title, self.posted_by)

class Report(models.Model):
    reporter = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    reason = models.CharField(
        max_length=16,
        help_text = "why are you reporting this?",
        choices=(
            ("hatespeech", "Contains hate Speech"),
            ("wrong_channel", "Channel is not appropriate"),
            ("wrong_rating", "Rating is not appropriate"),
            ("wrong_language", "Language is not appropriate"),
            ("other", "Other")
        )
    )
    note = models.CharField(
        max_length=255,
        help_text="do you have note for admins?",
        null=True,
        blank=True
    )
    reported_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def get_link_url(self):
        # needed to show admin list
        return self.link.get_absolute_url()

    def __unicode__(self):
        return "%s's report for %s" % (self.reporter, self.reason)
