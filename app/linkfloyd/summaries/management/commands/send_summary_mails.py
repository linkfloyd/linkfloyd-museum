from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from preferences.models import UserPreferences
from summaries.models import Unseen
from django.contrib.sites.models import Site
class Command(BaseCommand):
    args = 'daily | weekly | monthly'
    help = 'Builds and sends summary mails for given period'

    def handle(self, *args, **options):
        if not len(args) == 1:
            raise CommandError("Give a period please")

        period = args[0]

        if not period in ("daily", "weekly", "monthly"):
            raise CommandError("Period must be daily, weekly or monthly.")

        users = [preference.user for preference in
                 UserPreferences.objects.filter(summary_mails=period)]

        for user in users:

            unseen_links = [unseen.link for unseen in
                            Unseen.objects.filter(user=user)]

            if unseen_links:
                send_mail(
                    "%s new links for you:" % len(unseen_links),
                    render_to_string("summaries/body.txt", {
                        "user": user,
                        "links": unseen_links,
                        "site": Site.objects.get_current()
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email,],
                    fail_silently=False
                )

                self.stdout.write("Summary email for %s sent" % user)
