from django.conf import settings
from django.db import models

from accounts.models import CustomUser as User


class Consent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="retimgann_consent"
    )
    consented = models.BooleanField(default=False)


class Image(models.Model):
    image = models.ImageField(upload_to="annotate/")
    name = models.CharField(max_length=100, blank=True)
    # description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    coordinates = models.JSONField()
