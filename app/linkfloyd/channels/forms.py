from django import forms
from channels.models import Channel
from django.contrib.sites.models import Site

class CreateChannelForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete':'off'}))

    slug = forms.CharField(
        help_text= "http://%s/links/channel/<span id='slug_preview'></span>/" % Site.objects.get_current().domain,
        widget=forms.TextInput(attrs={'autocomplete':'off'}))

    class Meta:
        model = Channel
        exclude = ["is_official",]
    class Media:
        js = ("js/libs/jquery.slugify.js",)
