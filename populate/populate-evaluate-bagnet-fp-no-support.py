import glob
import os
import sys

from django.utils import timezone

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
import django

django.setup()

from django.contrib.auth import get_user_model

from retimgeval.models import SubQuestion, Task  # import the updated models

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
alias = "bagnet-fp-grading-no-support"
task = Task(
    description="Grading of DR without decision support from AI",
    category="bagnet",
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/evaluate/BagNetFP/no_support/*.png"))
num_images = len(all_images)

for i, img in enumerate(all_images):
    j = i + 1

    # Create the main question first
    main_question = task.question_set.create(
        description=f"Question {j}/{num_images}",
        created_at=timezone.now(),
        slug=f"{alias}-q{j}",
        image1=f"{img[6:]}",
        image1_width=512,
        image1_height=512,
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
