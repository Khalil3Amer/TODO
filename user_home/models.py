from django.db import models

from user_auth.models import User


class Task(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    deadline = models.DateTimeField(null=True)
    STATUS_CHOICES = [
        (False, "Not Completed"),
        (True, "Completed"),
    ]
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)

    def __str__(self):
        return self.name
