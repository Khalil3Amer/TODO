from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_info, name="user_info"),
    path("new_email/", views.change_email, name="new_email"),
    path("new_image/", views.change_image, name="new_image"),
    path("new_password/", views.change_password, name="new_password"),
]
