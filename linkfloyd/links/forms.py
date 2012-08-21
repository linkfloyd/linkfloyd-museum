from django import forms
from links.models import Link
from channels.models import Channel

class SubmitLinkForm(forms.ModelForm):

    body = forms.CharField(widget=forms.Textarea, required=False)

    channel = forms.ModelChoiceField(
        widget=forms.TextInput,
        required=True,
        queryset=Channel.objects.all()
    )

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

class UpdateLinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ['body', 'channel', 'rating']

    class Media:
        js = (
            "js/autofill.js",
            "js/libs/jquery.tokeninput.js",
            "js/csrf_fix.js"
        )

"""
class SubmitReportForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ['reporter',]
"""
