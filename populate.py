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
from retimgeval.models import Choice, Question, Task

User = get_user_model()

# Create a superuser

user = User.objects.create_user("admin", password="admin")
user.is_superuser = True
user.is_staff = True
user.save()

# Retinal Image Annotation

all_images = sorted(glob.glob("media/annotate/*.png"))

for image in all_images:
    img = Image(image=image[6:], name=image.split("/")[-1].split(".")[0])
    img.save()

# Retinal Image Evaluation

# task 1
t1 = Task(description="Task 1")
t1.save()

all_image_t1 = sorted(glob.glob("media/evaluate/Task1/*.png"))
num_img_set_t1 = len(set([img[:-5] for img in all_image_t1])) + 1
for img_set in range(1, num_img_set_t1):
    q = t1.question_set.create(
        description=f"[Task 1] Q{img_set}: which of the following is fake?",
        image1=f"evaluate/Task1/{img_set}a.png",
        image2=f"evaluate/Task1/{img_set}b.png",
        image3=f"evaluate/Task1/{img_set}c.png",
        created_at=timezone.now(),
        slug=f"t1q{img_set}p1",
    )
    for choice in ["a", "b", "c"]:
        q.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

# task 2
t2 = Task(description="Task 2 - condtion 1")
t2.save()

all_image_t2c1 = sorted(glob.glob("media/evaluate/Task2/cond1/*.png"))
num_img_set_t2c1 = len(set([img[:-4] for img in all_image_t2c1])) + 1
for img in range(1, num_img_set_t2c1):
    q1 = t2.question_set.create(
        description=f"[Task 2/1] Q{img}.1: Diabetic Retinopathy referral",
        image1=f"evaluate/Task2/cond1/{img}.png",
        created_at=timezone.now(),
        slug=f"t2q{img}p1",
    )

    for choice in ["No DR", "Referable DR"]:
        q1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    q2 = t2.question_set.create(
        description=f"[Task 2/1] Q{img}.2: How confident are you of the assigned grade?",
        created_at=timezone.now(),
        image1=f"evaluate/Task2/cond1/{img}.png",
        slug=f"t2q{img}p2",
    )

    for choice in range(1, 11):
        q2.choice_set.create(
            choice_text=f"{choice}",
        )


t3 = Task(
    description="Task 2 - condtion 2",
    created_at=timezone.now(),
)
t3.save()

all_image_t2c2 = sorted(glob.glob("media/evaluate/Task2/cond2/*.png"))
num_img_set_t2c2 = len(set([img[:-5] for img in all_image_t2c2])) + 1
for img in range(1, num_img_set_t2c2):
    q1 = t3.question_set.create(
        description=f"[Task 2/2] Q{img}.1: Question: Diabetic Retinopathy referral",
        created_at=timezone.now(),
        image1=f"evaluate/Task2/cond2/{img}a.png",
        image2=f"evaluate/Task2/cond2/{img}b.png",
        image3=f"evaluate/Task2/cond2/{img}c.png",
        slug=f"t3q{img}p1",
    )

    for choice in ["No DR", "Referable DR"]:
        q1.choice_set.create(
            choice_text=f"{choice}",
        )

    q2 = t3.question_set.create(
        description=f"[Task 2/2] Q{img}.2: How confident are you of the assigned grade?",
        created_at=timezone.now(),
        image1=f"evaluate/Task2/cond2/{img}a.png",
        image2=f"evaluate/Task2/cond2/{img}b.png",
        image3=f"evaluate/Task2/cond2/{img}c.png",
        slug=f"t3q{img}p2",
    )

    for choice in range(1, 11):
        q2.choice_set.create(
            choice_text=f"{choice}",
        )
