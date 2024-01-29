# Generated by Django 4.1.7 on 2023-07-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("retimgeval", "0003_task_alias"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="image1_height",
            field=models.PositiveIntegerField(default=256),
        ),
        migrations.AddField(
            model_name="question",
            name="image1_width",
            field=models.PositiveIntegerField(default=256),
        ),
        migrations.AddField(
            model_name="question",
            name="image2_height",
            field=models.PositiveIntegerField(default=256),
        ),
        migrations.AddField(
            model_name="question",
            name="image2_width",
            field=models.PositiveIntegerField(default=256),
        ),
        migrations.AddField(
            model_name="question",
            name="image3_height",
            field=models.PositiveIntegerField(default=256),
        ),
        migrations.AddField(
            model_name="question",
            name="image3_width",
            field=models.PositiveIntegerField(default=256),
        ),
    ]