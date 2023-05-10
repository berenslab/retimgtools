from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    experience = models.IntegerField(
        verbose_name="year of experience", blank=True, null=True
    )
