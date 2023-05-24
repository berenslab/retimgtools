from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, View

from .forms import AnswerForm, ConsentForm
from .models import Answer, Choice, Consent, Question, Task


class TaskInstructionView(CreateView):
    def get(self, request, alias):
        task = Task.objects.get(alias=alias)
        # Check if a Consent record already exists
        already_consented = False
        try:
            consent = Consent.objects.get(user=request.user, task=task)
            if consent.consented:
                already_consented = True
        except Consent.DoesNotExist:
            pass

        form = ConsentForm()
        context = {"task": task, "form": form, "already_consented": already_consented}
        return render(request, "retimgeval/task_instruction.html", context)

    def post(self, request, alias):
        form = ConsentForm(request.POST)
        task = Task.objects.get(alias=alias)
        if form.is_valid() and form.cleaned_data.get("consented") is True:
            consent, _ = Consent.objects.update_or_create(
                user=request.user,
                task=task,
                defaults={"consented": form.cleaned_data.get("consented")},
            )
            consent.save()
            return redirect("retimgeval:question_detail", slug=f"{alias}-q1p1")
        else:
            context = {"task": task, "form": form}
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
            return redirect("retimgeval:thank_you", alias=task.alias)

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
            option.delay_time = request.POST.get("delay_time", None)
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
                return redirect("retimgeval:thank_you", alias=task.alias)

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
        "reaction_time": request.GET.get("reaction_time", None),
        "delay_time": request.GET.get("delay_time", None),
    }

    return render(request, "retimgeval/question_detail.html", context)


class ThankYouPageView(View):
    def get(self, request, alias):
        task = Task.objects.get(alias=alias)
        next_task = (
            Task.objects.filter(category=task.category, alias__gt=task.alias)
            .order_by("alias")
            .first()
        )

        if next_task:
            next_link = reverse(
                "retimgeval:task_instruction", kwargs={"alias": next_task.alias}
            )
        else:
            next_link = None

        context = {
            "task": task,
            "next_link": next_link,
        }

        return render(request, "retimgeval/thank_you.html", context)
