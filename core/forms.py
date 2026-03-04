from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['resourcename', 'description', 'availability', 'course', 
                  'category', 'lenderid']
