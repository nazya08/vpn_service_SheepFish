"""
Forms for the site_management app.
"""
from django import forms

from site_management.models.website import Website


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'original_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'original_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
