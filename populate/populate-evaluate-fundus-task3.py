import glob
import os
import sys

# Add the project directory to the sys.path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

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

######################
# Separate questions #
######################

# # fundus task 2 part 1
# t3alias = "realism-fundus-grading-no-support-2"
# t3 = Task(
#     description="Grading of DR",
#     category="realism-fundus",
#     is_active=False,
#     alias=t3alias,
# )
# t3.save()

# all_image_t3 = sorted(glob.glob("media/evaluate/Fundus/Task3/*.png"))
# num_img_set_t3 = len(set([img[:-4] for img in all_image_t3]))
# for img in range(1, num_img_set_t3 + 1):
#     q1 = t3.question_set.create(
#         description=f"Q{img}/{num_img_set_t3} [1/2]: Diabetic Retinopathy referral",
#         image1=f"evaluate/Fundus/Task3/{img}.png",
#         created_at=timezone.now(),
#         slug=f"{t3alias}-q{img}p1",
#     )

#     for choice in ["No DR", "Referable DR"]:
#         q1.choice_set.create(
#             choice_text=f"{choice}",
#             created_at=timezone.now(),
#         )

#     q2 = t3.question_set.create(
#         description=f"Q{img}/{num_img_set_t3} [2/2]: How confident are you of the assigned grade?",
#         created_at=timezone.now(),
#         image1=f"evaluate/Fundus/Task2/cond1/{img}.png",
#         slug=f"{t3alias}-q{img}p2",
#     )

#     for choice in range(1, 11):
#         q2.choice_set.create(
#             choice_text=f"{choice}",
#         )


################
# Subquestions #
################


# Grading of DR without decision support
alias_without_support = "realism-fundus-grading-without-support-2"
task_without_support = Task(
    description="Grading of DR",
    category="realism-fundus",
    is_active=True,
    alias=alias_without_support,
)
task_without_support.save()

all_images_without_support = sorted(glob.glob("media/evaluate/Fundus/Task3/*.png"))
num_images_without_support = len(all_images_without_support)

for img_num in range(1, num_images_without_support + 1):
    # Create the main question first
    main_question = task_without_support.question_set.create(
        description=f"Question {img_num}/{num_images_without_support}",
        created_at=timezone.now(),
        image1=f"evaluate/Fundus/Task3/{img_num}.png",
        slug=f"{alias_without_support}-q{img_num}",
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
