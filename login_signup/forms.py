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
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        help_text="confirm your password",
    )
    name = forms.CharField(help_text="e.g. John Doe")
    email = forms.EmailField(
        help_text="john_doe@example.com",
        error_messages={"unique": "This email has already exists"},
    )

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            self.add_error(
                "password", "password and password confirm does not match"
            )


class UserLoginForm(forms.Form):
    email = forms.EmailField(help_text="john_doe@example.com")
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="your password",
    )

    class Meta:
        model = User
        fields = ["email", "password"]


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(help_text="Your email address", required=True)


class NewPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[password_check],
        help_text="AbcD1234",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        help_text="confirm your password",
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            self.add_error(
                "password", "password and password confirm does not match"
            )
