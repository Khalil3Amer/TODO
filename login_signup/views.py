from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserSignUpForm
from .models import User


def signup(request: HttpRequest):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Account created")
            return redirect("/")
        else:
            messages.warning(request, "invalid inputs!")
    form = UserSignUpForm()
    context = {"title": "Sign Up", "form": form}
    return render(request, "signup.html", context)


def login(request: HttpRequest):
    if request.session.exists("user_id"):
        return redirect("/home/")
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data["email"])
            if user.exists():
                user = user.first()
                if check_password(
                    form.cleaned_data["password"], user.password
                ):
                    request.session["user_id"] = user.id
                    return redirect("/home/")
                else:
                    messages.warning(request, "email/password are incorrect")
            else:
                messages.warning(request, "User not found")
    form = UserLoginForm()
    context = {"title": "Login", "form": form}
    return render(request, "login.html", context)


def forgot_password(request: HttpRequest):
    pass


def home(request):
    return render(request, "home.html", {"title": "Home"})
