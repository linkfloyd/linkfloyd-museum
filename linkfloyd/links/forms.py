from django import forms
from links.models import Link, Report 

from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class ThumbnailInput(Input):
    input_type = 'thumbnail'
    def __init__(self, attrs=None, render_value=False):
        super(ThumbnailInput, self).__init__(attrs)
        self.render_value = render_value

    def render(self, name, value, attrs=None):
        template = u'<div id="thumbnail_preview">'\
                   u'    <img src="{value}">'\
                   u'    <input type="hidden" id="{id}" name="{name}" value="{value}"/>'\
                   u'</div>'

        id = attrs.pop('id')

        return mark_safe(
            template.format(
                id=id,
                value=value or "",
                name=name
            )
        )

class SubmitLinkForm(forms.ModelForm):
    url = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
	help_text=_("paste url of your link here"),
	required=False)

    title = forms.CharField(
	widget=forms.TextInput(attrs={'autocomplete':'off'}),
	max_length=144,
	help_text=_("give a descriptive title to your link"))

    thumbnail_url = forms.URLField(
        label='Thumbnail',
        help_text=mark_safe(
            u'Is it looking bad?' \
            u'<a href="#" id="remove_thumbnail">click here</a> to remove.'),
        widget=ThumbnailInput,
        required=False)

    player = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False)

    description = forms.CharField(
        widget=forms.widgets.Textarea,
	help_text=_("say something about that link, use your words."))

    class Meta:
        model = Link
        exclude = ['posted_by', 'is_banned', 'is_sponsored', 'shown',
                   'vote_score', 'comment_score']

    class Media:
        js = ("js/autofill.js", "js/libs/jquery.tokeninput.js",)

    def __init__(self, *args, **kwargs):
        super(SubmitLinkForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance:
            self.fields['thumbnail_url'].widget.is_hidden=True
        else:
            if not instance.thumbnail_url:
                self.fields['thumbnail_url'].widget.is_hidden=True

        self.fields.keyOrder = [
	    'url',
            'channel',
            'title',
            'description',
            'language',
            'rating',
            'thumbnail_url',
            'player']

class EditLinkForm(SubmitLinkForm):
    def __init__(self, *args, **kwargs):
        super(EditLinkForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [\
            'channel',
            'title',
            'description',
            'language',
            'rating',
	    'thumbnail_url',
            'player']

    class Meta:
        model = Link
        exclude = ['posted_by', 'is_banned', 'is_sponsored', 'shown',
                   'vote_score', 'comment_score', 'url']

class SubmitReportForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ['reporter',]

