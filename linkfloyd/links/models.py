from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.utils.translation import ugettext as _

from django.db import models
from django.db.models import Sum

from channels.models import Channel
from channels.models import Subscription as ChannelSubscription

from qhonuskan_votes.models import VotesField

from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from qhonuskan_votes.models import vote_changed

from django.dispatch import receiver

SITE_RATINGS = (
    (1, _("Safe Posts (only safe content)")),
    (2, _("Moderate (can contain nudity, rude gestures)")),
    (3, _("Liberal (hell yeah.)")),
)

class Link(models.Model):
    posted_by = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=512, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=144, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    rating = models.PositiveIntegerField(
        choices=SITE_RATINGS,
        help_text=_("warn people about your link")
    )
    votes = VotesField()
    shown = models.PositiveIntegerField(default=0)
    player = models.TextField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)
    channel = models.ForeignKey(Channel)
    vote_score = models.PositiveIntegerField(default=0)
    comment_score = models.PositiveIntegerField(default=0)

    def get_domain(self):
        from urllib2 import urlparse
        return urlparse.urlparse(self.url).hostname

    def get_absolute_url(self):
        return "/links/%s/" % self.id

    def get_full_url(self):
        return "http://" + \
            Site.objects.get_current().domain + \
            self.get_absolute_url()

    def get_editing_url(self):
        return "/links/edit/%s/" % self.id

    def get_sharing_url(self):
        return "%s?site=%s" % (Site.objects.get_current().domain, self.url)

    def inc_shown(self):
        self.shown += 1
        self.save()

    def __unicode__(self):
        return u"%s by %s" % (self.title, self.posted_by)


class Subscription(models.Model):
    """We're holding unsubscriptions instead of subscriptions.
    * if subscription exists and subscripted=True, user subscripted
    * if subscription does not exists, user not subscripted
    * if subscription exists and subscripted=False, user unsubsubscripted
    """
    user = models.ForeignKey(User, related_name="link_unsubscriptions")
    link = models.ForeignKey(Link)
    status = models.PositiveSmallIntegerField(null=True, blank=True, choices=(
        (0, "unsubscribed"), (1, "subscribed")))


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
        return self.link.get_absolute_url()

    def __unicode__(self):
        return "%s's report for %s" % (self.reporter, self.reason)


@receiver(post_save, sender=Link, dispatch_uid="link_saved")
def link_saved(sender, **kwargs):

    from summaries.models import Unseen

    if kwargs['created'] == True:
        link = kwargs['instance']
        subscriptions = ChannelSubscription.objects.filter(channel=link.channel)
        for subscription in subscriptions:
            Unseen.objects.get_or_create(user=subscription.user, link=link)

        LinkSubscription = Subscription
        LinkSubscription.objects.get_or_create(link=link, user=link.posted_by,
            status=1)


@receiver(pre_delete, sender=Link, dispatch_uid="link_deleted")
def link_deleted(sender, **kwargs):
    from summaries.models import Unseen
    link = kwargs['instance']
    Unseen.objects.filter(link=link).delete()

@receiver(vote_changed)
def update_vote_score(sender, dispatch_uid="update_vote_score", **kwargs):
    link = sender.object
    link.vote_score = link.votes.aggregate(score=Sum('value'))['score']
    link.save()

