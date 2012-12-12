from django import forms


class GetImagesForm(forms.Form):
    url = forms.URLField()
    min_size = forms.IntegerField(required=False)
