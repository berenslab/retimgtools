# Generated by Django 4.2.1 on 2023-05-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitationcode",
            name="code",
            field=models.CharField(default="eeicpegh", max_length=100, unique=True),
        ),
    ]