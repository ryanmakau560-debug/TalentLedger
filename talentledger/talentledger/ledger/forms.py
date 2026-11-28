from django import forms
from .models import Session, Skill
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Session
from django import forms
from .models import Session

class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'start_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # <--- THIS IS THE KEY
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
        }
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
class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'start_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter session topic'}),
        }
class SessionBookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition'
            })
class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'start_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded mt-1', 
                'placeholder': 'e.g., Intro to Swimming'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'w-full p-2 border border-gray-300 rounded mt-1'
            }),
        }
        from django import forms
from .models import Session

class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'start_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none'
            }),
        }
        
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




