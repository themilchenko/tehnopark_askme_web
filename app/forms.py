from django import forms
from app import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ['user']


class CreateQuestion(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['title_text', 'question_text', 'tag_field']


class UpdateProfile(UserChangeForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.Profile
        exclude = ['user']


class SignInForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))
