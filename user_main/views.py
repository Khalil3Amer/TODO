from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import NewTaskForm


def main(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request, "main.html", {"title": "Main"})


def signout(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    logout(request)
    return redirect("/")


def new_task(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_id = request.user
            task.save()
            messages.success(
                request,
                "Task Added",
            )
        else:
            for errorKind, contents in form.errors.as_data().items():
                msg = errorKind.capitalize() + ":"
                for content in contents:
                    msg += content.message + "\n"
                messages.warning(request, msg)
    form = NewTaskForm()
    context = {"title": "New Task", "form": form}
    return render(request, "new_task.html", context)
