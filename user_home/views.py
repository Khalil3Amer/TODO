from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render

from .forms import NewTaskForm
from .models import Task


def main(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    user = request.user
    tasks = user.task_set.all()
    return render(request, "main.html", {"title": "Main", "user_tasks": tasks})


def signout(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    logout(request)
    return redirect("/")


def new_task(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        form = NewTaskForm()
        context = {"title": "New Task", "form": form}
        return render(request, "new_task.html", context)
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


def update_states(request: HttpRequest, task_id, is_compleated):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        user = request.user
        try:
            task = user.task_set.get(id=task_id)
            task.status = True
            if is_compleated == "false":
                task.status = False
            task.save()
            return JsonResponse({"valid": True}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"valid": False}, status=200)
    return JsonResponse({}, status=400)


def update_task(request: HttpRequest, task_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            try:
                task_to_update: Task = request.user.task_set.get(id=task_id)
                task_to_update.name = form.cleaned_data["name"]
                task_to_update.description = form.cleaned_data["description"]
                task_to_update.deadline = form.cleaned_data["deadline"]
                task_to_update.save()
                return redirect("/main")
            except ObjectDoesNotExist:
                messages.warning(request, "No such task!")
                return redirect("/main/new_task/")
    context = None
    try:
        form = NewTaskForm(initial=model_to_dict(Task.objects.get(id=task_id)))
        context = {"title": "Update Task", "form": form}
    except ObjectDoesNotExist:
        messages.warning(request, "No such task!")
        return redirect("/main/new_task/")
    return render(request, "update_task.html", context)


def delete_task(request: HttpRequest, task_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        user = request.user
        try:
            task = user.task_set.get(id=task_id)
            task.delete()
            return JsonResponse({"valid": True}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"valid": False}, status=200)
    return JsonResponse({}, status=400)
