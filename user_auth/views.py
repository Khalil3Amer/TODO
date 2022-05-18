from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from .forms import (
    NewPasswordForm,
    ResetPasswordForm,
    UserLoginForm,
    UserSignUpForm,
)
from .models import User


def show_error_msgs(request, form):
    for errorKind, contents in form.errors.as_data().items():
        msg = errorKind.capitalize() + ":"
        for content in contents:
            msg += content.message + "\n"
        messages.warning(request, msg)


def anonymous_required(function=None, redirect_url=None):

    if not redirect_url:
        redirect_url = "/main"

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url,
        redirect_field_name=None,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def signup(request: HttpRequest):
    if request.method == "GET":
        form = UserSignUpForm()
        context = {"form": form}
        return render(request, "signup.html", context)
    form = UserSignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data["password"])
        user.save()
        messages.success(
            request,
            mark_safe(_("Account Created: <a href='/login'>Login?</a>")),
        )
        return redirect("/")
    else:
        show_error_msgs(request, form)


@anonymous_required
def login(request: HttpRequest):
    if request.method == "GET":
        form = UserLoginForm()
        context = {"form": form}
        return render(request, "login.html", context)
    form = UserLoginForm(request.POST)
    if form.is_valid():
        umail = form.cleaned_data["email"]
        upasswd = form.cleaned_data["password"]
        user = authenticate(request=request, email=umail, password=upasswd)
        if user is not None:
            log_in(request, user)
            return redirect("/main/")
        else:
            messages.warning(request, _("email/password are incorrect"))
    form = UserLoginForm()
    context = {"form": form}
    return render(request, "login.html", context)


@anonymous_required
def forgot_password(request: HttpRequest):
    if request.method == "GET":
        form = ResetPasswordForm()
        context = {"form": form}
        return render(request, "password/password_reset.html", context)

    form = ResetPasswordForm(request.POST)
    if form.is_valid():
        user = User.objects.filter(email=form.cleaned_data["email"])
        if user.exists():
            user = user.first()
            subject = "Password Reset Requested"
            content = {
                "email": user.email,
                "site_name": "TODO",
                "domain": "localhost:8000",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "http",
            }
            email = render_to_string("password/reset_email_body.txt", content)
            try:
                send_mail(
                    subject,
                    email,
                    "password_reset@TODO.com",
                    [user.email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse(_("Invalid header found."))
            return render(
                request,
                "password/password_confirm.html",
            )
        else:
            messages.warning(
                request,
                mark_safe(_("Email not found: <a href='/signup'>Signup?</a>")),
            )


@anonymous_required
def new_password(request: HttpRequest, uidb64, token):
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=urlsafe_base64_decode(uidb64))
            if user.exists():
                user = user.first()
                user.password = make_password(form.cleaned_data["password"])
                user.save()
                return render(request, _("password/reset_done.html"))
        else:
            show_error_msgs(request, form)

    user = User.objects.filter(id=urlsafe_base64_decode(uidb64))
    if user.exists():
        user = user.first()
        if not default_token_generator.check_token(user, token):
            messages.warning(
                request, _("Invalid link please login or signup to continue.")
            )
            return redirect("/")
        form = NewPasswordForm()
        context = {"form": form}
        return render(request, "password/new_password.html", context)

    else:
        messages.warning(
            request,
            mark_safe(_("Email not found: <a href='/signup'>Signup</a>")),
        )
        return redirect("/")


@anonymous_required
def home(request: HttpRequest):
    return render(request, "home.html")
