from django.test import TestCase
from preferences.models import UserPreferences
from django.contrib.auth.models import User


class UserPreferencesTest(TestCase):
    def test_creating_user_preference(self):
        """
        When we try to get non existing user preference, it must be
        created on the fly.
        """
        # We have a user
        u1 = User.objects.create_user('u1', 'u1@u1.com', 'u1')

        # We don't have any UserPreferences at db.
        self.assertEqual(UserPreferences.objects.count(), 0,)

        # We're requesting it
        p1 = UserPreferences.objects.get(user=u1)

        # We have a UserPreference at p1
        self.assertEqual(isinstance(p1, UserPreferences), True)
