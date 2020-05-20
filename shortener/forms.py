from django import forms

from shortener.models import URL


class CreateLinkForm(forms.ModelForm):
    class Meta:
        model = URL
        exclude = ('short_link', 'owner')
