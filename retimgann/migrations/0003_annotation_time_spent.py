# Generated by Django 4.2.1 on 2023-05-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("retimgann", "0002_alter_annotation_coordinates_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="annotation",
            name="time_spent",
            field=models.FloatField(blank=True, null=True),
        ),
    ]