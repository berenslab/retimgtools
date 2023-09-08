import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

import glob

import pandas as pd
from django.contrib.auth import get_user_model
from django.utils import timezone

from retimgeval.models import SubQuestion, Task  # Import SubQuestion

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
        return f"AI model predicts:<br><strong>healthy</strong> ({row.confidence.values[0] * 100:.0f}% confidence)."
    else:
        return f"AI model predicts:<br><strong>DR</strong> ({row.confidence.values[0] * 100:.0f}% confidence)."


for i, img in enumerate(all_images):
    j = i + 1

    # Create the main question first
    main_question = task.question_set.create(
        description=f"Question {j}/{num_images}",
        created_at=timezone.now(),
        image1=f"{img[6:]}",
        image1_title=get_image_title(img[6:].split("/")[-1]),
        slug=f"{alias}-q{j}",
    )

    # Sub-question 1
    sub_question1 = main_question.subquestion_set.create(
        description=f"Does the patient have Diabetic Retinopathy (including mild DR)?",
        created_at=timezone.now(),
    )

    for choice in ["No DR", "DR"]:
        sub_question1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    # Sub-question 2
    sub_question2 = main_question.subquestion_set.create(
        description=f"How confident are you of the assigned grade?",
        created_at=timezone.now(),
    )

    for choice in range(1, 6):
        sub_question2.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )
