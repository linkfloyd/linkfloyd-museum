from django import forms as forms
from models import Page


class PageForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea())

    def clean_name(self):
        import re
        from templatetags.wiki import WIKI_WORD

        pattern = re.compile(WIKI_WORD)

        name = self.cleaned_data['name']
        if not pattern.match(name):
            raise forms.ValidationError('Must be a WikiWord.')

        return name

    def clean_translation_of(self):
        try:
            page = Page.objects.filter(
                language_id=self.cleaned_data['language'],
                translation_of=self.cleaned_data['translation_of']
            ).exclude(id=self.cleaned_data['id'])
        except:
            page = None

        if page:
            raise forms.ValidationError('That already have a translation')

        return self.cleaned_data['translation_of']

    class Meta:
        model = Page
        exclude = ('content_as_html', 'listed', 'contributors')
