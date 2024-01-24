import os

from django.db import migrations, models


def update_image_paths(apps, schema_editor):
    Image = apps.get_model("retimgann", "Image")
    for image in Image.objects.all():
        # Split the original path to get the filename
        path_parts = image.image.name.split("/")
        filename = path_parts[-1]  # Get the last part, which should be the filename
        # Construct the new path
        new_path = os.path.join("annotate", "fundus", filename)
        image.image.name = new_path
        image.save()


def reverse_image_paths(apps, schema_editor):
    # Reverse function (optional)
    # If you want to reverse the migration, you would do the opposite here.
    # This is more complex in this case and may not be necessary.
    pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "retimgann",
            "0009_alter_task_description",
        ),  # Make sure this dependency is correct
    ]

    operations = [
        migrations.RunPython(update_image_paths, reverse_image_paths),
    ]
