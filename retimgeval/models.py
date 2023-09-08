from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from PIL import Image as PilImage

User = get_user_model()


class Task(models.Model):
    description = models.TextField()
    category = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alias = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self, *args, **kwargs):
        if self.alias == "realism-fundus" or self.alias == "realism-oct":
            return reverse(
                "retimgeval:question_detail",
                kwargs={"slug": f"{self.alias}-q1"},
            )
        else:
            return reverse(
                "retimgeval:question_detail",
                kwargs={"slug": f"{self.alias}-q1p1"},
            )


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    image1 = models.ImageField(upload_to="images/", blank=True, null=True)
    image1_title = models.CharField(max_length=200, blank=True, null=True)
    image1_width = models.PositiveIntegerField(default=256)
    image1_height = models.PositiveIntegerField(default=256)

    image2 = models.ImageField(upload_to="images/", blank=True, null=True)
    image2_title = models.CharField(max_length=200, blank=True, null=True)
    image2_width = models.PositiveIntegerField(default=256)
    image2_height = models.PositiveIntegerField(default=256)

    image3 = models.ImageField(upload_to="images/", blank=True, null=True)
    image3_title = models.CharField(max_length=200, blank=True, null=True)
    image3_width = models.PositiveIntegerField(default=256)
    image3_height = models.PositiveIntegerField(default=256)

    image4 = models.ImageField(upload_to="images/", blank=True, null=True)
    image4_title = models.CharField(max_length=200, blank=True, null=True)
    image4_width = models.PositiveIntegerField(default=256)
    image4_height = models.PositiveIntegerField(default=256)

    image5 = models.ImageField(upload_to="images/", blank=True, null=True)
    image5_title = models.CharField(max_length=200, blank=True, null=True)
    image5_width = models.PositiveIntegerField(default=256)
    image5_height = models.PositiveIntegerField(default=256)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.image1:
            image1 = PilImage.open(self.image1.path)
            self.image1_width, self.image1_height = image1.size
        if self.image2:
            image2 = PilImage.open(self.image2.path)
            self.image2_width, self.image2_height = image2.size
        if self.image3:
            image3 = PilImage.open(self.image3.path)
            self.image3_width, self.image3_height = image3.size

        if self.image4:
            image4 = PilImage.open(self.image4.path)
            self.image4_width, self.image4_height = image4.size

        if self.image5:
            image5 = PilImage.open(self.image5.path)
            self.image5_width, self.image5_height = image5.size

        super().save(*args, **kwargs)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    answered_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    reaction_time = models.FloatField(blank=True, null=True)
    delay_time = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.choice.choice_text

    def get_absolute_url(self):
        return reverse(
            "question:question_detail",
            kwargs={"slug": f"t{self.task.pk}q{self.question.pk}p1"},
        )


class Consent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="retimgeval_consent"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    consented = models.BooleanField(default=False)
    consented_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
