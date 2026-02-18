from django import forms
from .models import Photo, Profile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'title']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Write a caption...', 'class': 'form-control'})
        # Description is removed as per request

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            placeholder = field.label
            if field.required:
                placeholder += ' *'
            field.widget.attrs.update({'placeholder': placeholder})

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 1
            })
        }
