from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):

    shared_by = models.ForeignKey(User)
    url = models.URLField()
    title = models.CharField(max_length=2048, blank=True)
    description = models.CharField(max_length=4096, blank=True)
    thumbnail_url = models.URLField()
    rating = models.CharField(
        max_length=2,
        choices=(
            ("G", "Suitable with any audience type."),
            ("PG", "This link can contain rude gestures, provocatively dressed individuals, the lesser swear words, or mild violence"),
            ("R",  "This link may contain such things as harsh profanity, intense violence, nudity, or hard drug use."),
            ("X",  "This link may contain hardcore sexual imagery or extremely disturbing violence.")
        ),
        help_text = "Choose rating."
    )
    is_banned = models.BooleanField(default=False)
    published_at = models.BooleanField(default=False)

    def get_absolute_url(self):
        return "/link/%s/" % self.id

    def get_sharing_url(self):
        return "%s?site=%s" % (Site.objects.get_current().domain, self.url)

    def __unicode__(self):
        return self.url
