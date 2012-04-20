from django import forms
from links.models import Link, Report, SITE_RATINGS

from django.forms.util import flatatt
from django.forms.widgets import Input
from django.utils.safestring import mark_safe

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
        max_length=4096,
        widget=forms.widgets.Textarea,
        required=False)

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
            else:
                self.fields['thumbnail_url'].widget.is_hidden=False


class EditLinkForm(SubmitLinkForm):
    class Meta:
        model = Link
        exclude = ['posted_by', 'is_banned', 'is_sponsored', 'shown',
                   'vote_score', 'comment_score', 'url']

class SubmitReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ['reporter',]

