from django import forms
from .models import *

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'url']
