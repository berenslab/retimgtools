from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from retimgann.models import Annotation, Image
from retimgeval.models import Answer, Question, Task

from .forms import CustomUserCreationForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


from django.contrib.auth import get_user_model

# class AccountDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"
#     template_name = "accounts/account_detail.html"
#     all_tasks = Task.objects.all()
#     all_images = Image.objects.all()
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from retimgann.models import Annotation, Image
from retimgeval.models import Answer, Question, Task

User = get_user_model()


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "accounts/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get all images and tasks
        images = Image.objects.all()
        tasks = Task.objects.all()

        # Get IDs of annotated images and answered questions by this user
        annotated_images = Annotation.objects.filter(user=user).values_list(
            "image", flat=True
        )
        answered_questions = Answer.objects.filter(user=user).values_list(
            "question", flat=True
        )

        # Filter images and questions to annotate/evaluate
        images_to_annotate = images.exclude(id__in=annotated_images)
        questions_to_evaluate = Question.objects.exclude(id__in=answered_questions)

        context.update(
            {
                "annotated_images": annotated_images,
                "answered_questions": answered_questions,
                "images_to_annotate": images_to_annotate,
                "questions_to_evaluate": questions_to_evaluate,
            }
        )

        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User

    fields = [
        "username",
        "experience",
    ]

    template_name = "accounts/account_update.html"

    def get_success_url(self):
        return reverse("home")

    def get_object(self):
        return User.objects.get(username=self.request.user.username)
