from django.conf import settings
from django.db import models

from accounts.models import CustomUser as User


class Consent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="retimgann_consent"
    )
    consented = models.BooleanField(default=False)
    consented_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Task(models.Model):
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=255)  # Add this line
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alias = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.alias


class Image(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="annotate/")
    name = models.CharField(max_length=100, blank=True)
    index = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    coordinates = models.JSONField(default=list)
    time_spent = models.FloatField(blank=True, null=True)
    mouse_trajectory = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        unique_together = [["user", "image"]]
