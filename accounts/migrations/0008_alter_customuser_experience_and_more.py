# Generated by Django 4.1.7 on 2023-07-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_alter_invitationcode_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="experience",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name="Number of  of years of experience in medical retina",
            ),
        ),
        migrations.AlterField(
            model_name="invitationcode",
            name="code",
            field=models.CharField(default="udimqnvb", max_length=100, unique=True),
        ),
    ]