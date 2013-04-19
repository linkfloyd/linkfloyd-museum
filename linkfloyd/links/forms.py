from django import forms
from links.models import Link
from channels.models import Channel


class SubmitLinkForm(forms.ModelForm):
    url = forms.URLField(verify_exists=False)

    title = forms.CharField(
        required=False,
        max_length=255)

    thumbnail_url = forms.URLField(
        required=False,
        widget=forms.HiddenInput)

    thumbnail_offset = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput)

    channel = forms.ModelChoiceField(
        required=True,
        queryset=Channel.objects.all())

    player = forms.CharField(
        required=False,
        widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'title',
            'url',
            'description',
            'channel',
            'rating',
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
        js = ('js/autofill.js',)


class UpdateLinkForm(SubmitLinkForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'title',
            'description',
            'channel',
            'rating',
            'thumbnail_url',
            'player']

    class Meta:
        model = Link
        fields = ['title', 'description', 'channel', 'rating']

    class Media:
        js = (
            "js/autofill.js",
            "js/csrf_fix.js"
        )
