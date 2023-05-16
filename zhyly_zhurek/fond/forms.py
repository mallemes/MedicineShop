from django.contrib.auth.forms import UserCreationForm
from django import forms
from fond.models import MyUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))

    class Meta:
        model = MyUser
        fields = ["username", "email", "password1", "password2", "avatar"]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name']
