from django.db import models
from links.models import Link
from django.contrib.auth.models import User

class Unseen(models.Model):
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
