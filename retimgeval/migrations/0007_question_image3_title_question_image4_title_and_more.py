# Generated by Django 4.2.2 on 2023-09-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("retimgeval", "0006_question_image1_title_question_image2_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="image3_title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="image4_title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="image5_title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
