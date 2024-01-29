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

alias = "erm-oct"
task = Task(
    description="ERM Detection for OCT",
    category=alias,
    is_active=True,
    alias=alias,
)
task.save()

all_images = sorted(glob.glob("media/evaluate/ERM-OCT/*.png"))
num_images = len(all_images)


for i, img in enumerate(all_images):
    j = i + 1

    # Create the main question first
    main_question = task.question_set.create(
        description=f"Image {j}/{num_images}",
        created_at=timezone.now(),
        slug=f"{alias}-q{j}",
        image1=f"{img[6:]}",
        image1_width=675 * 1.5,
        image1_height=300 * 1.5,
    )

    # Sub-question 1
    sub_question1 = main_question.subquestion_set.create(
        description=f"Does the heatmap correctly indicate ERM evidence?",
        created_at=timezone.now(),
    )

    for choice in [
        "Strongly Agree",
        "Somewhat Agree",
        "Not Sure",
        "Somewhat Disagree",
        "Strongly Disagree",
    ]:
        sub_question1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    # Sub-question 2
    sub_question2 = main_question.subquestion_set.create(
        description=f"How confident are you?",
        created_at=timezone.now(),
    )

    for choice in range(1, 6):
        sub_question2.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )
