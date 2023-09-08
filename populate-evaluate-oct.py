import glob
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

from retimgeval.models import SubQuestion, Task  # Import the updated models

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
    # Create the main question first
    main_question = task.question_set.create(
        description=f"Question {img_set}/{num_img_set}: Which image was generated by AI?",
        image1=f"evaluate/OCT/Task1/{img_set}a.png",
        image2=f"evaluate/OCT/Task1/{img_set}b.png",
        image3=f"evaluate/OCT/Task1/{img_set}c.png",
        created_at=timezone.now(),
        slug=f"{alias}-q{img_set}",
    )

    # Sub-question
    sub_question = main_question.subquestion_set.create(
        description="Please select the image generated by AI.",
        created_at=timezone.now(),
    )

    # Choices for the sub-question
    for choice in ["a", "b", "c"]:
        sub_question.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )
