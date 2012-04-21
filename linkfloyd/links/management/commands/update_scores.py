from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from django.db.models import Sum

from links.models import Link

class Command(BaseCommand):
    help = "updates comment and vote scores of links"

    def handle(self, *args, **options):
        for link in Link.objects.all():
            link.vote_score = link.votes.aggregate(score=Sum('value'))['score']
            link.comment_score = link.comment_set.all().count()
            link.save()
