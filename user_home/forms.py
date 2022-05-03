from django import forms
from django.utils import timezone

from .models import Task


class NewTaskForm(forms.ModelForm):
    name = forms.CharField(
        help_text="A new task name",
    )
    description = forms.CharField(
        widget=forms.Textarea, help_text="Task description"
    )
    deadline = forms.DateTimeField(
        help_text="when you wish to finish this task?",
        widget=forms.TextInput(attrs={"type": "datetime-local"}),
        required=False,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline"]

    def clean(self):
        cleaned_data = super().clean()
        current_datetime = timezone.now()
        deadline = cleaned_data.get("deadline")
        if deadline is None:
            self.add_error("deadline", "the deadline cannot be empty")
            return None
        if current_datetime > deadline:
            self.add_error(
                "deadline", "the deadline cannot be before this time"
            )
        cleaned_data["deadline"] = deadline
        return cleaned_data
