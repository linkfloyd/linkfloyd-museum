from django import forms
from links.models import Link
from channels.models import Channel

class SubmitLinkForm(forms.ModelForm):

    body = forms.CharField(widget=forms.Textarea, required=False)

    title = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.HiddenInput)

    description = forms.CharField(
        required=False,
        max_length=2048,
        widget=forms.HiddenInput)

    thumbnail_url = forms.URLField(
        required=False,
        widget=forms.HiddenInput)

    channel = forms.ModelChoiceField(
        required=True,
        queryset=Channel.objects.all())

    player = forms.CharField(
        required = False,
        widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'url',
            'body',
            'channel',
            'rating',
            'title',
            'description',
            'thumbnail_url',
            'player'
        ]

    class Meta:
        model = Link
        exclude = ['posted_by',
                   'is_banned',
                   'is_sponsored',
                   'shown',
                   'vote_score',
                   'comment_score']

    class Media:
        js = ('js/autofill.js',
              'js/libs/jquery.tokeninput.js',
              'js/csrf_fix.js')

    def clean(self):

        cleaned_data = super(SubmitLinkForm, self).clean()

        if not (cleaned_data.get("body") or cleaned_data.get("url")):
            raise forms.ValidationError(\
                "Sending nothing? Please write something, or attach "
                "a link.")

        # Always return the full collection of cleaned data.
        return cleaned_data

class UpdateLinkForm(SubmitLinkForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'body',
            'channel',
            'rating',
            'title',
            'description',
            'thumbnail_url',
            'player']

    class Meta:
        model = Link
        fields = ['body', 'channel', 'rating']

    class Media:
        js = (
            "js/autofill.js",
            "js/libs/jquery.tokeninput.js",
            "js/csrf_fix.js"
        )
