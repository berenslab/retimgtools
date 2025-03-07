from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from PIL import Image as PilImage

User = get_user_model()


class Task(models.Model):
    """
    Represents a task with a description, category, and optional alias.
    Tasks can be active or inactive.
    """
    description = models.TextField()
    category = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alias = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self, *args, **kwargs):
        """
        Returns the absolute URL for the task's associated question.
        Special handling for specific aliases.

        The conditional logic is for backwards compatibility with the old
        version before the implementation of Subquestion.
        """
        if (
            self.alias == "realism-fundus-grading-no-support"
            or self.alias == "realism-fundus-grading-with-support"
        ):
            return reverse(
                "retimgeval:question_detail",
                kwargs={"slug": f"{self.alias}-q1p1"},
            )
        return reverse(
            "retimgeval:question_detail",
            kwargs={"slug": f"{self.alias}-q1"},
        )


class Question(models.Model):

    """
    Represents a question associated with a task.
    It can have up to three images with associated titles and dimensions.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    image1 = models.ImageField(
        upload_to="images/", blank=True, null=True, max_length=255
    )
    image1_title = models.CharField(max_length=200, blank=True, null=True)
    image1_width = models.PositiveIntegerField(default=256)
    image1_height = models.PositiveIntegerField(default=256)

    image2 = models.ImageField(
        upload_to="images/", blank=True, null=True, max_length=255
    )
    image2_title = models.CharField(max_length=200, blank=True, null=True)
    image2_width = models.PositiveIntegerField(default=256)
    image2_height = models.PositiveIntegerField(default=256)

    image3 = models.ImageField(
        upload_to="images/", blank=True, null=True, max_length=255
    )
    image3_title = models.CharField(max_length=200, blank=True, null=True)
    image3_width = models.PositiveIntegerField(default=256)
    image3_height = models.PositiveIntegerField(default=256)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):

        """
        Overrides the save method to automatically update image dimensions.
        This avoids storing incorrect values when an image is uploaded.

        This will take precedence over the image dimensions set in the admin. 
        So if the image dimensions are set in the admin, they will be overwritten 
        by the actual image dimensions.
        """

        if self.image1 and not self.image1_width:
            image1 = PilImage.open(self.image1.path)
            self.image1_width, self.image1_height = image1.size
        if self.image2 and not self.image2_width:
            image2 = PilImage.open(self.image2.path)
            self.image2_width, self.image2_height = image2.size
        if self.image3 and not self.image3_width:
            image3 = PilImage.open(self.image3.path)
            self.image3_width, self.image3_height = image3.size
        super().save(*args, **kwargs)


class SubQuestion(models.Model):
    """
    Represents a sub-question under a specific question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, max_length=255
    )
    image_width = models.PositiveIntegerField(default=256)
    image_height = models.PositiveIntegerField(default=256)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.image and not self.image_width:
            image = PilImage.open(self.image.path)
            self.image_width, self.image_height = image.size
        super().save(*args, **kwargs)


class Choice(models.Model):
    """
    Represents an answer choice for a question or sub-question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    sub_question = models.ForeignKey(
        SubQuestion, on_delete=models.CASCADE, null=True, blank=True
    )
    choice_text = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, max_length=255
    )
    image_width = models.PositiveIntegerField(default=256)
    image_height = models.PositiveIntegerField(default=256)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.choice_text

    def save(self, *args, **kwargs):
        if self.image and not self.image_width:
            image = PilImage.open(self.image.path)
            self.image_width, self.image_height = image.size
        super().save(*args, **kwargs)


class Answer(models.Model):
    """
    Stores user answers to questions and sub-questions.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    sub_question = models.ForeignKey(
        SubQuestion, on_delete=models.CASCADE, null=True, blank=True
    )
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    answered_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    reaction_time = models.FloatField(blank=True, null=True)
    delay_time = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.choice.choice_text

    def get_absolute_url(self):
        return reverse(
            "question:question_detail",
            kwargs={"slug": f"t{self.task.pk}q{self.question.pk}p1"},
        )


class Consent(models.Model):
    """
    Tracks whether a user has consented to a specific task.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="retimgeval_consent"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    consented = models.BooleanField(default=False)
    consented_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
