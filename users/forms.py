from django import forms
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm

from datetime import date

from .models import Profile, Message


class CustomSignUpForm(SignupForm):
    birthday = forms.DateField()

    def clean_birthday(self):
        dob = self.cleaned_data['birthday']
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('You must be at least 18 years old to register')
        return dob

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2', 'birthday')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your bio', 'rows': 5}),
        }
        fields = ('first_name', 'last_name', 'location', 'birthday', 'bio')
        labels = {
            'first_name': (''),
            'last_name': (''),
            'location': (''),
            'birthday': (''),
            'bio': ('')
        }


class ProfilePicForm(forms.ModelForm):
    avatar = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'style': 'display: none;'}))
    class Meta:
        model = Profile
        fields = ('avatar', )


class MessageForm(forms.ModelForm):
    message = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
    class Meta:
        model = Message
        fields = ('message',)
        labels = {
            'message': ('')
        }


class MessageReadForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('unread', )