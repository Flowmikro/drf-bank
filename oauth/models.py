from decimal import Decimal

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models

from oauth.manager import CustomUserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                  validators=[MinValueValidator(Decimal('0.01'))])

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return str(self.id)
