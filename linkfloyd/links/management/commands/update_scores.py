from django.core.management.base import BaseCommand

from django.db.models import Sum

from links.models import Link

class Command(BaseCommand):
    help = "updates comment and vote scores of links"

    def handle(self, *args, **options):
        for link in Link.objects.all():
            link.vote_score = \
                link.votes.aggregate(score=Sum('value'))['score'] or 0
            link.comment_score = link.comment_set.all().count()
            link.save()
