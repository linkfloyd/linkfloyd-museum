from django import forms
from preferences.models import UserPreferences

class UpdatePreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        exclude = ['user',]
