from django import forms
from .models import Skill
from django import forms

from talentledger.ledger.models import Session


class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'start_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded mt-1'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'w-full p-2 border border-gray-300 rounded mt-1'
            }),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'proficiency': forms.Select(attrs={'class': 'border p-2 w-full rounded'}),
        }