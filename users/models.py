from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)

    # Ratings
    time_spent = models.PositiveIntegerField(default=0, editable=0)
    findings_count = models.PositiveIntegerField(default=0, editable=0)
    rating = models.PositiveIntegerField(default=0, editable=0)

