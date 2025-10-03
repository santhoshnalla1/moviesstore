from django import forms
from .models import Petition
from movies.models import Movie

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title','description','movie']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}