from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("signout/", views.signout, name="signout"),
    path("new_task/", views.new_task, name="new_task"),
    path(
        "update_status/<task_id>/<is_compleated>",
        views.update_states,
        name="update_states",
    ),
    path("update_task/<int:task_id>", views.update_task, name="update_task"),
    path("delete_task/<int:task_id>", views.delete_task, name="delete_task"),
]
