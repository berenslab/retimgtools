import os
import sys

# Add the project directory to the sys.path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

import glob

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from retimgann.models import Image, Task

User = get_user_model()


# Create a superuser

try:
    user = User.objects.create_user("admin", password="admin")
    user.is_superuser = True
    user.is_staff = True
    user.save()
except:
    pass


# OCT Image Annotation
alias = "annotate-oct"
task = Task(
    title="OCT Image Annotation",
    category=alias,
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/annotate/OCT/*.png"))

for index, image in enumerate(all_images):
    img = Image(
        task=task,
        image=image[6:],
        name=image.split("/")[-1].split(".")[0],
        index=index + 1,
    )
    img.save()
