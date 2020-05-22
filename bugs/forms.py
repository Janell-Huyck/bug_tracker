from django import forms

# New Ticket


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)


# class MyUserForm(forms.Form):
#     username = forms.CharField(
#         max_length=50)
#     display_name = forms.CharField(max_length=50)
#     password = forms.CharField(
#         widget=forms.PasswordInput, max_length=20)

#     home_page = forms.URLField(
#         max_length=200, required=False)
#     age = forms.IntegerField(required=False)


class TicketForm(forms.Form):
    title = forms.CharField(max_length=100)
    details = forms.CharField(widget=forms.Textarea)


"""

class Ticket(models.Model):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    INVALID = "INVALID"

    TICKET_STATUS_CHOICES = [
        (NEW, "New"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (INVALID, "Invalid"),
    ]

    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="creator"
    )
    title = models.CharField(max_length=100)
    details = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        default="",
        null=True,
        blank=True,
        related_name="asignee",
    )
    completed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        default="",
        null=True,
        blank=True,
        related_name="completor",
    )
    status = models.CharField(
        max_length=12, choices=TICKET_STATUS_CHOICES, default="NEW"
    )
    

User
    username    charfield
    password    charfield
    email       email field
    first name
    last name
    tagline

Forms Needed:
New User Signup
?? change ticket status for dropdown in detail
Edit Ticket


"""
