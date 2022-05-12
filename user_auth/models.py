from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django_softdelete.models import SoftDeleteModel
from model_utils.models import TimeStampedModel


def password_check(passwd):
    if len(passwd) < 8:
        raise ValidationError("length should be at least 8")

    if not any(char.isdigit() for char in passwd):
        raise ValidationError("Password should have at least one numeral")

    if not any(char.isupper() for char in passwd):
        raise ValidationError(
            "Password should have at least one uppercase letter"
        )

    if not any(char.islower() for char in passwd):
        raise ValidationError(
            "Password should have at least one lowercase letter"
        )


class User(SoftDeleteModel, TimeStampedModel, AbstractBaseUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    image = models.ImageField(null=True, blank=True)
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name
