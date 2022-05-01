from django import forms

from login_signup.models import User


class NewEmailForm(forms.Form):
    new_email = forms.EmailField(
        help_text="john_doe@example.com",
        error_messages={"unique": "This email has already exists"},
    )


class NewImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image"]
