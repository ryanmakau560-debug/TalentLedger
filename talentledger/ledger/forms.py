from django import forms
from .models import Skill
from django.contrib.auth.forms import UserCreationForm
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category']  # Updated to match your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'category': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
        }

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'border p-2 w-full rounded'})

