from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from user_auth.views import show_error_msgs

from .forms import NewEmailForm, NewImageForm, NewPasswordForm


def user_info(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request, "user_info.html")


def change_email(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = NewEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data["new_email"]
            request.user.save()
            messages.success(request, "Email Updated")
            return redirect("/profile")
    form = NewEmailForm()
    context = {"form": form}
    return render(request, "new_email.html", context)


def change_image(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = NewImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Image Updated"))
            return redirect("/profile")
    form = NewImageForm(instance=request.user)
    context = {"form": form}
    return render(request, "new_image.html", context)


def change_password(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        form = NewPasswordForm()
        context = {"form": form}
        return render(request, "new_image.html", context)
    form = NewPasswordForm(request.POST)
    if form.is_valid():
        if request.user.check_password(form.cleaned_data["old_password"]):
            request.user.password = form.clean()["password"]
            request.user.save()
            messages.success(request, _("Password Updated"))
            return redirect("/profile")
        else:
            messages.warning(request, _("Wrong Password"))
    else:
        show_error_msgs(request, form)
