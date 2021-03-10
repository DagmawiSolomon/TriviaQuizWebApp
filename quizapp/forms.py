from django import forms
from .models import Result


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Result
        fields = ('profile',)