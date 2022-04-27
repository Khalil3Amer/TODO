from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UserSignUpForm


def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created")
            return redirect("/")
        else:
            messages.warning(request, "invalid inputs!")
    form = UserSignUpForm()
    context = {"title": "Sign Up", "form": form}
    return render(request, "signup.html", context)


def home(request):
    return render(request, "home.html", {"title": "Home"})
