import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


# Invitation code model
def generate_random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


class InvitationCode(models.Model):
    code = models.CharField(
        max_length=100, unique=True, default=generate_random_string()
    )
    is_used = models.BooleanField(default=False)


# User model


class CustomUser(AbstractUser):
    experience = models.IntegerField(
        verbose_name="Number of  of years of experience in medical retina",
        blank=True,
        null=True,
    )
    code_used = models.CharField(max_length=100, null=True, blank=True)
