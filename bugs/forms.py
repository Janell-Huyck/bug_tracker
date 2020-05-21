from django import forms


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=50)
#     password = forms.CharField(widget=forms.PasswordInput, max_length=20)


# class MyUserForm(forms.Form):
#     username = forms.CharField(
#         max_length=50)
#     display_name = forms.CharField(max_length=50)
#     password = forms.CharField(
#         widget=forms.PasswordInput, max_length=20)

#     home_page = forms.URLField(
#         max_length=200, required=False)
#     age = forms.IntegerField(required=False)


"""
User
    username    charfield
    password    charfield
    email       email field
    first name
    last name
    tagline

Ticket
    title   charfield
    details textarea
    created at datetime - autocomplete this
    status - choice field New, In Progress, Done, Invalid - start as new
    created by - many-1 - autocreate - who's logged in
    assigned to - many-1 - start as none, Foreignkey
    completed by - many-1   Foreignkey
    


Forms Needed:
New Ticket
New User Signup
?? change ticket status for dropdown in detail
Edit Ticket


"""
