from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, View

from .forms import AnswerForm, ConsentForm
from .models import Answer, Choice, Consent, Question, Task


class LandingPageView(CreateView):
    model = Consent
    form_class = ConsentForm
    template_name = "retimgeval/landing_page.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user has already given consent
            user_consent = Consent.objects.filter(
                user=request.user, consented=True
            ).first()
            if user_consent:
                # If user has given consent, redirect to the annotation page
                return redirect("retimgeval:task_list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect("retimgeval:task_list")


class TaskInstructionView(View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        context = {"task": task}
        return render(request, "retimgeval/task_instruction.html", context)


# Create your views here.
def task_list(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "retimgeval/task_list.html", context)


def get_next_unanswered_question(request, current_task):
    unanswered_questions = (
        Question.objects.filter(task=current_task)
        .exclude(answer__user=request.user)
        .order_by("pk")
    )

    if unanswered_questions:
        return unanswered_questions.first()
    else:
        return None


def question_detail(request, slug):
    question = Question.objects.get(slug=slug)
    task = Task.objects.get(pk=question.task.pk)

    if Answer.objects.filter(question=question, user=request.user).exists():
        # This question has already been answered
        next_question = get_next_unanswered_question(request, task)

        if next_question:
            # There is another question in this task
            return redirect("retimgeval:question_detail", slug=next_question.slug)
        else:
            # This was the last question in this task
            return redirect("retimgeval:thank_you", pk=task.pk)

    choices = question.choice_set.all()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        form.question = question
        form.fields["choice"].queryset = Choice.objects.filter(
            question_id=form.question.pk
        )

        if form.is_valid():
            option = form.save(commit=False)
            option.reaction_time = request.POST.get("reaction_time", None)
            option.task = task
            option.question = question
            option.user = request.user
            option.save()

            next_question = get_next_unanswered_question(request, task)
            if next_question:
                # There is another question in this task
                return redirect("retimgeval:question_detail", slug=next_question.slug)
            else:
                # This was the last question in this task
                return redirect("retimgeval:thank_you", pk=task.pk)

    else:
        form = AnswerForm()
        form.question = question
        form.fields["choice"].queryset = Choice.objects.filter(
            question_id=form.question.pk
        )

    context = {
        "question": question,
        "choices": choices,
        "form": form,
        # read ajax response
        "reaction_time": request.GET.get("reaction_time", None),
    }

    return render(request, "retimgeval/question_detail.html", context)


class ThankYouPageView(View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        next_task = Task.objects.filter(pk__gt=task.pk).order_by("pk").first()

        if next_task:
            next_link = reverse(
                "retimgeval:task_instruction", kwargs={"pk": next_task.pk}
            )
        else:
            next_link = None

        context = {
            "task": task,
            "next_link": next_link,
        }

        return render(request, "retimgeval/thank_you.html", context)
