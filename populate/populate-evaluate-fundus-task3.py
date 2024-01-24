import glob
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

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

# Grading of DR with decision support
alias_with_support = "realism-fundus-grading-with-support"
task_with_support = Task(
    description="Grading of DR with decision support from AI",
    category="realism-fundus",
    is_active=True,
    alias=alias_with_support,
)
task_with_support.save()

all_images_with_support = sorted(glob.glob("media/evaluate/Fundus/Task2/cond2/*.png"))
num_images_with_support = (
    len(all_images_with_support) // 3
)  # Assuming 3 images per question

for img_num in range(1, num_images_with_support + 1):
    # Create the main question first
    main_question = task_with_support.question_set.create(
        description=f"Question {img_num}/{num_images_with_support}",
        created_at=timezone.now(),
        image1=f"evaluate/Fundus/Task2/cond2/{img_num}a.png",
        image2=f"evaluate/Fundus/Task2/cond2/{img_num}b.png",
        image3=f"evaluate/Fundus/Task2/cond2/{img_num}c.png",
        slug=f"{alias_with_support}-q{img_num}",
    )

    # Sub-question 1: Diabetic Retinopathy referral
    sub_question1 = main_question.subquestion_set.create(
        description=f"Diabetic Retinopathy Referal",
        created_at=timezone.now(),
    )
    for choice in ["No DR", "Referable DR"]:
        sub_question1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    # Sub-question 2: How confident are you of the assigned grade?
    sub_question2 = main_question.subquestion_set.create(
        description=f"How confident are you of the assigned grade?",
        created_at=timezone.now(),
    )
    for choice in range(1, 6):
        sub_question2.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )
