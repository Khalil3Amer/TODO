from django.db import models

from login_signup.models import User


class Task(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    deadline = models.DateTimeField(null=True)
    STATUS_CHOICES = [
        ("Not Completed", "Not Completed"),
        ("Completed", "Completed"),
    ]
    status = models.CharField(
        max_length=13,
        choices=STATUS_CHOICES,
        default="Not Completed",
    )

    def __str__(self):
        return self.name
