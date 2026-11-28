# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add your custom fields here
    credit_balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username