from django import forms

from .models import User, password_check


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
