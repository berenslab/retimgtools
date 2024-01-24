from django.db import migrations


def create_initial_task(apps, schema_editor):
    Task = apps.get_model("retimgann", "Task")
    Task.objects.create(
        title="Lesion annotation for diabetic retinopathy",
        description="",  # Fill in as needed
        category="bagnet-fundus",
        is_active=False,
        alias="bagnet-fundus",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("retimgann", "0006_task"),
    ]

    operations = [
        migrations.RunPython(create_initial_task),
    ]
