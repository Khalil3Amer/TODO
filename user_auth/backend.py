from django.contrib.auth.backends import ModelBackend

from .models import User


class NewBackend(ModelBackend):
    def authenticate(self, request, email, password) -> User:
        try:
            user: User = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
