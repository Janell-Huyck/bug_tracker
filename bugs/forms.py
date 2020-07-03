from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)


class CustomUserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    tag_line = forms.CharField(max_length=200)


class TicketForm(forms.Form):
    title = forms.CharField(max_length=100)
    details = forms.CharField(widget=forms.Textarea)


"""


User
    username    charfield
    password    charfield
    email       email field
    first name
    last name
    tagline

Forms Needed:
New User Signup


"""
