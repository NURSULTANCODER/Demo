from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    grade = models.DecimalField(max_digits=1, decimal_places=1, default=0.0)
