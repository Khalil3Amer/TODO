from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.home, name="home"),
    path("login/",views.login, name="login"),
    path("forget_password/",views.login, name="forget_password"),
]
