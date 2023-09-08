from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, View

from .forms import AnswerForm, ConsentForm
from .models import Answer, Choice, Consent, Question, SubQuestion, Task


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
            return redirect("retimgeval:question_detail", slug=f"{alias}-q1")
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
    try:
        question = Question.objects.get(slug=slug)
        task = Task.objects.get(pk=question.task.pk)
    except (Question.DoesNotExist, Task.DoesNotExist):
        raise Http404("Question or Task not found")

    if Answer.objects.filter(question=question, user=request.user).exists():
        next_question = get_next_unanswered_question(request, task)
        if next_question:
            return redirect("retimgeval:question_detail", slug=next_question.slug)
        else:
            return redirect("retimgeval:thank_you", alias=task.alias)

    sub_questions = SubQuestion.objects.filter(question=question)

    if request.method == "POST":
        for sub_question in sub_questions:
            choice_id = request.POST.get(
                str(sub_question.id), None
            )  # Get choice id for each sub-question
            form_data = {"choice": choice_id}
            form = AnswerForm(form_data)
            form.fields["choice"].queryset = sub_question.choice_set.all()

            if form.is_valid():
                answer = form.save(commit=False)
                answer.reaction_time = request.POST.get("reaction_time", None)
                answer.delay_time = request.POST.get("delay_time", None)
                answer.task = task
                answer.question = question
                answer.sub_question = sub_question  # This assumes your Answer model has a sub_question field
                answer.user = request.user
                answer.save()
            else:
                print(
                    f"Form is not valid for sub_question {sub_question.id}: {form.errors}"
                )
                return render(
                    request,
                    "retimgeval/question_detail.html",
                    {"form_errors": form.errors},
                )

        next_question = get_next_unanswered_question(request, task)
        if next_question:
            return redirect("retimgeval:question_detail", slug=next_question.slug)
        else:
            return redirect("retimgeval:thank_you", alias=task.alias)

    else:
        sub_questions_and_forms = []
        for sub_question in sub_questions:
            form = AnswerForm()
            form.fields["choice"].queryset = sub_question.choice_set.all()
            sub_questions_and_forms.append((sub_question, form))

    context = {
        "question": question,
        "sub_questions_and_forms": sub_questions_and_forms,
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
