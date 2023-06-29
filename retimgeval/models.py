from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

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
    image2 = models.ImageField(upload_to="images/", blank=True, null=True)
    image3 = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description


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
