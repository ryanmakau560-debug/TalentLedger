from django import forms
from .models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']  # Add any other fields you have in your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'proficiency': forms.Select(attrs={'class': 'border p-2 w-full rounded'}),
        }