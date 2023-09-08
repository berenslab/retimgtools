import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

import glob

import pandas as pd
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


# BagNet task 3
alias = "bagnet-grading-with-ai-support-and-bounding-boxes"
task = Task(
    description="Grading of DR with decision support and bounding boxes from AI",
    category="bagnet",
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/evaluate/BagNet/task3/All_images_with_bb/*.png"))
num_images = len(all_images)
all_images_inference = pd.read_csv(
    "media/evaluate/BagNet/grading_task_test_inference.csv"
)


def get_image_title(image_name):
    row = all_images_inference[all_images_inference["filename"] == image_name]
    if row.pred.values[0] == 0:
        return f"Our model predicted no signs of Onset 1 with {row.confidence.values[0] * 100:.2f}% confidence."
    else:
        return f"Our model predicted signs of Onset 1 with {row.confidence.values[0] * 100:.2f}% confidence."


for i, img in enumerate(all_images):
    j = i + 1
    q1 = task.question_set.create(
        description=f"Q{j}/{num_images} [1/2]: Are there signs of diabetic retinopathy Onset 1?",
        image1=f"{img[6:]}",
        image1_title=get_image_title(img[6:].split("/")[-1]),
        created_at=timezone.now(),
        slug=f"{alias}-q{j}p1",
    )

    for choice in ["No signs of Onset 1", "There are signs of Onset 1"]:
        q1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    q2 = task.question_set.create(
        description=f"Q{j}/{num_images} [2/2]: How confident are you of the assigned grade?",
        created_at=timezone.now(),
        image1=f"{img[6:]}",
        image1_title=get_image_title(img[6:].split("/")[-1]),
        slug=f"{alias}-q{j}p2",
    )

    for choice in range(1, 11):
        q2.choice_set.create(
            choice_text=f"{choice}",
        )
