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

# Retinal Image Annotation

all_images = sorted(glob.glob("media/annotate/*.png"))

for index, image in enumerate(all_images):
    img = Image(
        image=image[6:],
        name=image.split("/")[-1].split(".")[0],
        index=index + 1,
    )
    img.save()

# Retinal Image Evaluation

# task 1
t1alias = "realism"
t1 = Task(
    description="Realism of AI-generated fundus images",
    category="realism",
    is_active=True,
    alias=t1alias,
)
t1.save()

all_image_t1 = sorted(glob.glob("media/evaluate/Task1/*.png"))
num_img_set_t1 = len(set([img[:-5] for img in all_image_t1]))
for img_set in range(1, num_img_set_t1 + 1):
    q = t1.question_set.create(
        description=f"Q{img_set}/{num_img_set_t1}: Which image is fake?",
        image1=f"evaluate/Task1/{img_set}a.png",
        image2=f"evaluate/Task1/{img_set}b.png",
        image3=f"evaluate/Task1/{img_set}c.png",
        created_at=timezone.now(),
        slug=f"{t1alias}-q{img_set}p1",
    )
    for choice in ["a", "b", "c"]:
        q.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

# task 2
t2alias = "realism-grading-no-support"
t2 = Task(
    description="Grading of DR without decision suppor",
    category="realism",
    is_active=True,
    alias=t2alias,
)
t2.save()

all_image_t2c1 = sorted(glob.glob("media/evaluate/Task2/cond1/*.png"))
num_img_set_t2c1 = len(set([img[:-4] for img in all_image_t2c1]))
for img in range(1, num_img_set_t2c1 + 1):
    q1 = t2.question_set.create(
        description=f"Q{img}/{num_img_set_t2c1} [1/2]: Diabetic Retinopathy referral",
        image1=f"evaluate/Task2/cond1/{img}.png",
        created_at=timezone.now(),
        slug=f"{t2alias}-q{img}p1",
    )

    for choice in ["No DR", "Referable DR"]:
        q1.choice_set.create(
            choice_text=f"{choice}",
            created_at=timezone.now(),
        )

    q2 = t2.question_set.create(
        description=f"Q{img}/{num_img_set_t2c1} [2/2]: How confident are you of the assigned grade?",
        created_at=timezone.now(),
        image1=f"evaluate/Task2/cond1/{img}.png",
        slug=f"t2q{img}p2",
    )

    for choice in range(1, 11):
        q2.choice_set.create(
            choice_text=f"{choice}",
        )

t3alias = "realism-grading-with-support"
t3 = Task(
    description="Grading of DR with decision support",
    category="realism",
    is_active=True,
    alias=t3alias,
)
t3.save()

all_image_t2c2 = sorted(glob.glob("media/evaluate/Task2/cond2/*.png"))
num_img_set_t2c2 = len(set([img[:-5] for img in all_image_t2c2]))
for img in range(1, num_img_set_t2c2 + 1):
    q1 = t3.question_set.create(
        description=f"Q{img}/{num_img_set_t2c2} [1/2]: Question: Diabetic Retinopathy referral",
        created_at=timezone.now(),
        image1=f"evaluate/Task2/cond2/{img}a.png",
        image2=f"evaluate/Task2/cond2/{img}b.png",
        image3=f"evaluate/Task2/cond2/{img}c.png",
        slug=f"{t3alias}-q{img}p1",
    )

    for choice in ["No DR", "Referable DR"]:
        q1.choice_set.create(
            choice_text=f"{choice}",
        )

    q2 = t3.question_set.create(
        description=f"Q{img}/{num_img_set_t2c2} [2/2]: How confident are you of the assigned grade?",
        created_at=timezone.now(),
        image1=f"evaluate/Task2/cond2/{img}a.png",
        image2=f"evaluate/Task2/cond2/{img}b.png",
        image3=f"evaluate/Task2/cond2/{img}c.png",
        slug=f"{t3alias}-q{img}p2",
    )

    for choice in range(1, 11):
        q2.choice_set.create(
            choice_text=f"{choice}",
        )


# task 4
t4alias = "bagnet-grading-no-support"
t4 = Task(
    description="Grading of DR without decision support",
    category="bagnet",
    is_active=False,
    alias=t4alias,
)
t4.save()

# task 5
t5alias = "bagnet-grading-with-support"
t5 = Task(
    description="Grading of DR with decision support",
    category="bagnet",
    is_active=False,
    alias=t5alias,
)
t5.save()
