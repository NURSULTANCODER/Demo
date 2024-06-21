from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    OWNER = 1
    EMPLOYEE = 2

    ROLE_CHOICES = (
        (OWNER, 'Owner'),
        (EMPLOYEE, 'Employee'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    grade = models.DecimalField(max_digits=1, decimal_places=1, default=0.0)

    REQUIRED_FIELDS = ['role']
