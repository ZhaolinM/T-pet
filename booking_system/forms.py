from django.contrib.auth.models import User
from django import forms

class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password',]
    password = forms.CharField(widget=forms.PasswordInput)