from django import forms
from django.contrib.auth.hashers import make_password

from user_auth.models import User, password_check


class NewEmailForm(forms.Form):
    new_email = forms.EmailField(
        help_text="john_doe@example.com",
        error_messages={"unique": "This email has already exists"},
    )


class NewImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image"]


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
