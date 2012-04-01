from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.template.loader import render_to_string
from django.conf import settings

from preferences.models import UserPreferences
from summaries.models import Unseen
from django.contrib.sites.models import Site
from optparse import make_option

from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    args = 'daily | weekly | monthly'
    help = 'Builds and sends summary mails for given period'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            action='store_true',
            dest='dry',
            default=False,
            help='Run without posting emails and writing them on stdout'),
        )

    def handle(self, *args, **options):
        if not len(args) == 1:
            raise CommandError("Give a period please")

        period = args[0]

        if not period in ("daily", "weekly", "monthly"):
            raise CommandError("Period must be daily, weekly or monthly.")

        users = [preference.user for preference in
                 UserPreferences.objects.filter(summary_mails=period)]

        for user in users:

            unseen_models = Unseen.objects.filter(user=user)
            unseen_links = [unseen.link for unseen in unseen_models]

            if unseen_links:
                email_title = "%s new links for you:" % len(unseen_links)
                email_body_txt = render_to_string("summaries/body.txt", {
                    "user": user,
                    "links": unseen_links,
                    "site": Site.objects.get_current()
                })
                email_body_html = render_to_string("summaries/body.html", {
                    "user": user,
                    "links": unseen_links,
                    "site": Site.objects.get_current()
                })

                email = EmailMultiAlternatives(
                    email_title,
                    email_body_txt,
                    "Linkfloyd %s" %settings.DEFAULT_FROM_EMAIL,
                    [user.email,])
                email.attach_alternative(email_body_html, "text/html")
                email.send()
                self.stdout.write("Summary email for %s sent\n" % user)
                if not options['dry']:
                    unseen_models.delete()
