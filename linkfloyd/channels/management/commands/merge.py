from django.core.management.base import BaseCommand, CommandError
from channels.models import Channel, Subscription
from links.models import Link
import sys

class Command(BaseCommand):
    args = '<channel_slug channel_slug>'
    help = 'Merges first channel to second channel with subscriptions'


c    def handle(self, *args, **options):
        if not len(args) == 2:
            raise CommandError('Please give source and destination channel slugs')

        source_channel_slug, dest_channel_slug= args[0], args[1]

        try:
            source_channel = Channel.objects.get(slug=source_channel_slug)
        except Channel.DoesNotExist:
            raise CommandError('Channel "%s" does not exist' % source_channel_slug)

        try:
            dest_channel = Channel.objects.get(slug=dest_channel_slug)
        except Channel.DoesNotExist:
            raise CommandError('Channel "%s" does not exist' % dest_channel_slug)

        confirmed = raw_input("Merge \"%s\" to \"%s\"? (y/n)" % (source_channel, dest_channel))

        if not confirmed == "y":
            sys.exit()

        self.stdout.write("Migrating links of source channel\n")
        self.stdout.write("---------------------------------\n\n")
		
        for link in Link.objects.filter(channel=source_channel):
            link.channel = dest_channel
            link.save()
            self.stdout.write("UPDATED: %s\n" % link)

        self.stdout.write("Migrating subscriptions to destination channel\n")
        self.stdout.write("----------------------------------------------\n\n")

        for subscription in Subscription.objects.filter(channel=source_channel):
            subscribed = Subscription.objects.filter(user=subscription.user, channel=subscription.channel).count()
            if subscribed:
                subscription.delete()
            else:
                subscription.channel = dest_channel
                subscription.save()

            self.stdout.write("UPDATED: %s\n" % subscription.user)

        source_channel.delete()
