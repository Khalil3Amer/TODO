from django.urls import path, re_path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    re_path("", views.home, name="home"),
]
