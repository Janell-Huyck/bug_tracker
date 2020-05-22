from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    tag_line = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username


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

    def __str__(self):
        return self.title

    def assign_ticket(self, username):
        self.assigned_to = CustomUser.objects.get(username=username)
        self.save()

    def change_status(self, new_status):
        self.status = new_status
        self.save()

    def complete_ticket(self, username):
        self.completed_by = CustomUser.objects.get(username=username)
        self.save()
