from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("signout/", views.signout, name="signout"),
    path("new_task/", views.new_task, name="new_task"),
]
