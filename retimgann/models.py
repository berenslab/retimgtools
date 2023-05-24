from django.conf import settings
from django.db import models

from accounts.models import CustomUser as User


class Consent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="retimgann_consent"
    )
    consented = models.BooleanField(default=False)
    consented_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Image(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        unique_together = [["user", "image"]]
