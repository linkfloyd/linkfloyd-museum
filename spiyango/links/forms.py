from django import forms
from links.models import Link, SITE_RATINGS
from taggit.forms import TagField

class SubmitLinkForm(forms.ModelForm):
    thumbnail_url = forms.URLField(
        widget=forms.widgets.HiddenInput,
        required=False)

    description = forms.CharField(
        max_length=4096,
        widget=forms.widgets.Textarea,
        required=False)

    """
    chaptcha = ReCaptchaField(
        public_key="6LfUAsoSAAAAALdaUVRrv-OArxpJ7JUd-Q9CQOI9",
        private_key="6LfUAsoSAAAAAJ3tkXCOQCa7H0s8ca4EiWQRUv8c",
        attrs={"theme": "white"},
        help_text= "Please type that two words to make us understand that you are human"
    )
    """

    tags = TagField()

    class Meta:
        model = Link
        exclude = ['posted_by', 'is_banned', 'shown']

    class Media:
        js = ("js/autofill.js", "js/libs/jquery.tagsinput.min.js",)
        css = {"all": ("css/libs/jquery.tagsinput.css",)}

class EditLinkForm(SubmitLinkForm):
    class Meta:
        model = Link
        exclude = ['url', 'posted_by', 'is_banned', 'shown']

