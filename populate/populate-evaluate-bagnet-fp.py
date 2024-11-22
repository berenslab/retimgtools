import csv
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
alias = "bagnet-fp"
task = Task(
    description="Grading of DR with decision support from AI",
    category="bagnet",
    is_active=True,
    alias=alias,
)
task.save()

# Load the CSV file
csv_file = "media/evaluate/BagNetFP/bagnet_fp_classification_30.csv"
filenames = []
with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        filenames.append(row["filename"])

# List all image files in both folders
images_without_support = sorted(glob.glob("media/evaluate/BagNetFP/no_support/*.png"))
images_with_support = sorted(glob.glob("media/evaluate/BagNetFP/with_support/*.png"))

# Filter images based on the filenames in the CSV
filtered_images_without_support = [
    img for img in images_without_support if os.path.basename(img) in filenames
]
filtered_images_with_support = [
    img for img in images_with_support if os.path.basename(img) in filenames
]

print(len(filtered_images_without_support), len(filtered_images_with_support))

# Ensure the lengths of both lists match
if len(images_without_support) != len(images_with_support):
    raise ValueError(
        "Mismatch in the number of images between the 'without_support' and 'with_support' folders."
    )

# Seed for pseudorandomization (you can set it to any integer value for consistency)
seed = 42
random.seed(seed)

# Pair the images and randomize them together
paired_images = list(zip(filtered_images_without_support, filtered_images_with_support))
random.shuffle(paired_images)

num_images = len(paired_images)

for i, (img_without_support, img_with_support) in enumerate(paired_images):
    j = i + 1

    # Create the main question first
    main_question = task.question_set.create(
        description=f"Question {j}/{num_images}",
        created_at=timezone.now(),
        slug=f"{alias}-q{j}",
        image1=f"{img_without_support[6:]}",  # Image without support
        image1_width=512,
        image1_height=512,
        image2=f"{img_with_support[6:]}",  # Image with support
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
        description=f"",
        created_at=timezone.now(),
    )
