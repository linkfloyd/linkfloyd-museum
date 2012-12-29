from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import signals

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("links_comment", _("Link Commented"), _("Some of links that you subscribed, has new comment"))
        notification.create_notice_type("links_upvote", _("Link Upvoted"), _("Some of links that you subscribed, has new upvote"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
