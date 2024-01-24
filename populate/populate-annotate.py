import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

import glob

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from retimgann.models import Image
from retimgeval.models import Task

User = get_user_model()

# Create a superuser

try:
    user = User.objects.create_user("admin", password="admin")
    user.is_superuser = True
    user.is_staff = True
    user.save()
except:
    pass

# Retinal Image Annotation

all_images = sorted(glob.glob("media/annotate/*.png"))

for index, image in enumerate(all_images):
    img = Image(
        image=image[6:],
        name=image.split("/")[-1].split(".")[0],
        index=index + 1,
    )
    img.save()
