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

alias = "erm-macula"
task = Task(
    description="ERM Detection for Macula",
    category=alias,
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/evaluate/ERM_Macula/*/img/*.png"))
num_images = len(all_images)


for i, img in enumerate(all_images):
    j = i + 1
    description = f"Image {j}/{num_images}"
    slug = f"{alias}-q{j}"
    print(f"{len(description)}", f"{len(slug)}")

    # Create the main question first
    main_question = task.question_set.create(
        description=f"Image {j}/{num_images}",
        created_at=timezone.now(),
        slug=slug,
        image1=f"{img[6:]}",
        image1_width=450 * 2,
        image1_height=300 * 2,
    )

    # Sub-question 1

    patch_path = "/".join(img.split("/")[:-2]) + "/patch"
    all_patches = sorted(glob.glob(f"{patch_path}/*.png"))

    for patch_id, patch in enumerate(all_patches):

        sub_question_patch = main_question.subquestion_set.create(
            description=f"{patch_id}",
            created_at=timezone.now(),
            image=f"{patch[6:]}",
            image_width=90,
            image_height=90,
        )

        for choice in ["Yes", "No", "Unsure"]:
            sub_question_patch.choice_set.create(
                choice_text=f"{choice}",
                created_at=timezone.now(),
            )

    # # Sub-question 2
    # sub_question_confidence = main_question.subquestion_set.create(
    #     description=f"How confident are you?",
    #     created_at=timezone.now(),
    # )

    # for choice in range(1, 6):
    #     sub_question_confidence.choice_set.create(
    #         choice_text=f"{choice}",
    #         created_at=timezone.now(),
    #     )
