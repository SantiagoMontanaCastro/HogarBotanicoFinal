from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu problema'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe tu problema'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }