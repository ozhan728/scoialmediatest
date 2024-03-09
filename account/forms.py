from django import forms

class UserRegistrationForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'your username','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email@site.com','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
