# Generated by Django 5.0.1 on 2024-01-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0016_alter_invitationcode_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitationcode",
            name="code",
            field=models.CharField(default="ybssxbqv", max_length=100, unique=True),
        ),
    ]