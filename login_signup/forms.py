from django import forms
from django.core.exceptions import ValidationError

from .models import User


def password_check(passwd):

    if len(passwd) < 8:
        raise ValidationError("length should be at least 8")

    if not any(char.isdigit() for char in passwd):
        raise ValidationError("Password should have at least one numeral")

    if not any(char.isupper() for char in passwd):
        raise ValidationError(
            "Password should have at least one uppercase letter"
        )

    if not any(char.islower() for char in passwd):
        raise ValidationError(
            "Password should have at least one lowercase letter"
        )


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[password_check],
        help_text="AbcD1234",
    )
    name = forms.CharField(help_text="e.g. John Doe")
    email = forms.EmailField(help_text="john_doe@example.com")

    class Meta:
        model = User
        fields = ["name", "email", "password"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(help_text="john_doe@example.com")
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="your password",
    )

    class Meta:
        model = User
        fields = ["email", "password"]
