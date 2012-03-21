from django.db import models
from links.models import Link
from django.contrib.auth.models import User
from utils import reduced_markdown

# Create your models here.

class Comment(models.Model):
    link = models.ForeignKey(Link)
    body = models.TextField()
    as_html = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, related_name="posted_by")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s's comment on %s" % (self.posted_by, self.link)

    def save(self, *args, **kwargs):
        from utils import reduced_markdown
        self.as_html = reduced_markdown(self.body, safe_mode="remove")
        super(Comment, self).save(*args, **kwargs)
