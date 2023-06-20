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

# OCT task 1
alias = "realism-oct"
task = Task(
    description="Realism of AI-generated OCT images",
    category="realism-oct",
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/evaluate/OCT/Task1/*.png"))
num_img_set = len(set([img[:-5] for img in all_images]))
for img_set in range(1, num_img_set + 1):
    q = task.question_set.create(
        description=f"Q{img_set}/{num_img_set}: Which image is fake?",
        image1=f"evaluate/OCT/Task1/{img_set}a.png",
        image2=f"evaluate/OCT/Task1/{img_set}b.png",
        image3=f"evaluate/OCT/Task1/{img_set}c.png",
        created_at=timezone.now(),
        slug=f"{alias}-q{img_set}",
    )
    for choice in ["a", "b", "c"]:
        q.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )
