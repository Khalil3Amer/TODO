from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from user_auth.views import show_error_msgs

from .forms import NewTaskForm
from .models import Task


@login_required(redirect_field_name=None, login_url="/login")
def main(request: HttpRequest):
    user = request.user
    tasks = user.task_set.all()
    return render(request, "main.html", {"user_tasks": tasks})


@login_required(redirect_field_name=None, login_url="/login")
def signout(request: HttpRequest):
    logout(request)
    return redirect("/")


@login_required(redirect_field_name=None, login_url="/login")
def new_task(request: HttpRequest):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(
                request,
                _("Task Added"),
            )
            return redirect("/")
        else:
            show_error_msgs(request, form)
    form = NewTaskForm()
    context = {"form": form}
    return render(request, "new_task.html", context)


@login_required(redirect_field_name=None, login_url="/login")
def update_states(request: HttpRequest, task_id, is_compleated):
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


@login_required(redirect_field_name=None, login_url="/login")
def update_task(request: HttpRequest, task_id):
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
                messages.warning(request, _("No such task!"))
                return redirect("/main/new_task/")
    context = None
    try:
        form = NewTaskForm(initial=model_to_dict(Task.objects.get(id=task_id)))
        context = {"form": form}
    except ObjectDoesNotExist:
        messages.warning(request, _("No such task!"))
        return redirect("/main/new_task/")
    return render(request, "update_task.html", context)


def delete_task(request: HttpRequest, task_id):
    if request.method == "GET":
        user = request.user
        try:
            task = user.task_set.get(id=task_id)
            task.delete()
            return JsonResponse({"valid": True}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"valid": False}, status=200)
    return JsonResponse({}, status=400)
