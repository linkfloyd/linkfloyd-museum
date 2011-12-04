from django import forms
from spiyango.links.models import Link, SITE_RATINGS

class SubmitLinkForm(forms.ModelForm):
    thumbnail_url = forms.URLField(
        widget=forms.widgets.HiddenInput,
        required=False)

    player = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False)

    description = forms.CharField(
        max_length=4096,
        widget=forms.widgets.Textarea,
        required=False)

    class Meta:
        model = Link
        exclude = ['posted_by', 'is_banned', 'shown']

    class Media:
        js = ("js/autofill.js", "js/libs/jquery.tokeninput.js",)
        css = {"all": ("css/libs/token-input.css",)}

class EditLinkForm(SubmitLinkForm):
    class Meta:
        model = Link
        exclude = ['url', 'posted_by', 'is_banned', 'shown']

