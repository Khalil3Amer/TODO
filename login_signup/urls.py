from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("forget_password/", views.forgot_password, name="forget_password"),
    path(
        "new_password/<uidb64>/<token>/",
        views.new_password,
        name="new_password",
    ),
]
