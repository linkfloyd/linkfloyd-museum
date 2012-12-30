from django.test import TestCase
from notifications.models import NotificationPreference
from notifications.models import NotificationType
from django.contrib.auth.models import User


class UserPreferencesTest(TestCase):
    def test_creating_notification_preference(self):

        # We have a user
        u1 = User.objects.create_user('u1', 'u1@u1.com', 'u1')

        for ntype in NotificationType.objects.all():

            # We don't have any UserPreferences at db.
            self.assertEqual(NotificationPreference.objects.filter(
                user=u1).count(), 0)

            # We're requesting it
            p1 = NotificationPreference.objects.get(user=u1, type=ntype)

            # We have a UserPreference at p1
            self.assertEqual(isinstance(p1, NotificationPreference), True)
