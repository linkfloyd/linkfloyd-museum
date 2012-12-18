from django.db import models
from markdown import markdown
from django.contrib.auth.models import User

class Page(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    content_as_html = models.TextField()
    listed = models.BooleanField()
    contributors = models.ManyToManyField(User)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.content_as_html = markdown(self.content, safe_mode="remove")
        super(Page, self).save(*args, **kwargs)
