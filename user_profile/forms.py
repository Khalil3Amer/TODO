from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from user_auth.models import User


class NewEmailForm(forms.Form):
    new_email = forms.EmailField(
        help_text="john_doe@example.com",
        error_messages={"unique": "This email has already exists"},
    )


class NewImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image"]


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


class NewPasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="your old password",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[password_check],
        help_text="your old password",
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        help_text="your old password",
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        password_confirm = cleaned_data.get("new_password_confirm")
        if password != password_confirm:
            self.add_error(
                "new_password", "password and password confirm does not match"
            )
            return None
        cleaned_data["password"] = make_password(cleaned_data["new_password"])
        return cleaned_data
