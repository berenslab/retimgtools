import glob
import os
import random
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
alias = "bagnet-fp-grading-with-support"
task = Task(
    description="Grading of DR with decision support from AI",
    category="bagnet",
    is_active=True,
    alias=alias,
)
task.save()

# List all image files
all_images_without_support = glob.glob("media/evaluate/BagNetFP/without_support/*.png")
all_images_with_support = glob.glob("media/evaluate/BagNetFP/with_support/*.png")

# Seed for pseudorandomization (you can set it to any integer value for consistency)
seed = 42

# Shuffle using the seed
random.seed(seed)
randomized_images_without_support = sorted(
    all_images_without_support, key=lambda x: random.random()
)
randomized_images_with_support = sorted(
    all_images_with_support, key=lambda x: random.random()
)

num_images = len(randomized_images_without_support)

for i, img in enumerate(randomized_images_without_support):
    j = i + 1

    # Create the main question first
    main_question = task.question_set.create(
        description=f"Question {j}/{num_images}",
        created_at=timezone.now(),
        slug=f"{alias}-q{j}",
        image1=f"{img[6:]}",
        image1_width=512,
        image1_height=512,
        image2=f"{img[6:]}",
        image2_width=512,
        image2_height=512,
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
        description=f"Do the bounding boxes contain DR related lesions?",
        created_at=timezone.now(),
    )

    for choice in ["Yes", "No"]:
        sub_question2.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )
