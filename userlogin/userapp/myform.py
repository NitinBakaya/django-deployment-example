from django import forms
from userapp.models import UserProfileInfo
from django.contrib.auth.models import User
from django.core import validators
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(),validators=[validators.MinLengthValidator(8)])

    class Meta():
        model = User
        fields = ('username','email','password')


class UserInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_site','profile_pic')
