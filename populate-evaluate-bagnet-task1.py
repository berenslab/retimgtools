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


# BagNet task 1
alias = "bagnet-grading-no-support"
task = Task(
    description="Grading of DR without decision support",
    category="bagnet-grading-no-support",
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/evaluate/BagNet/Task1/*.png"))
# num_img_set = len(set([img[:-4] for img in all_images]))
num_images = len(all_images)
for i, img in enumerate(all_images):
    q1 = task.question_set.create(
        description=f"Q{i}/{num_images} [1/2]: Diabetic Retinopathy referral",
        image1=f"{img[6:]}",
        created_at=timezone.now(),
        slug=f"{alias}-q{i}p1",
    )

    for choice in ["No DR", "Referable DR"]:
        q1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    q2 = task.question_set.create(
        description=f"Q{i}/{num_images} [2/2]: How confident are you of the assigned grade?",
        created_at=timezone.now(),
        image1=f"{img[6:]}",
        slug=f"{alias}-q{i}p2",
    )

    for choice in range(1, 11):
        q2.choice_set.create(
            choice_text=f"{choice}",
        )
