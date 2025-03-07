from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, View

from .forms import AnswerForm, ConsentForm
from .models import Answer, Choice, Consent, Question, SubQuestion, Task


class TaskInstructionView(LoginRequiredMixin, CreateView):
    """
    Displays task instructions and handles consent form submission.
    """
    def get(self, request, alias):
        """
        Handles GET request for displaying task instructions.
        Checks if the user has already consented to the task.
        """
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
        """
        Handles POST request for submitting consent form.
        If the form is valid and consent is given, the user is redirected to the first question.
        """
        form = ConsentForm(request.POST)
        task = Task.objects.get(alias=alias)
        if form.is_valid() and form.cleaned_data.get("consented") is True:
            consent, _ = Consent.objects.update_or_create(
                user=request.user,
                task=task,
                defaults={"consented": form.cleaned_data.get("consented")},
            )
            consent.save()
            if (
                task.alias == "realism-fundus-grading-no-support"
                or task.alias == "realism-fundus-grading-with-support"
            ):
                return redirect("retimgeval:question_detail", slug=f"{alias}-q1p1")
            else:
                return redirect("retimgeval:question_detail", slug=f"{alias}-q1")
        else:
            context = {"task": task, "form": form}
            return render(request, "retimgeval/task_instruction.html", context)


@login_required
def task_list(request):
    """
    Displays a list of available tasks.
    """
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "retimgeval/task_list.html", context)


@login_required
def get_next_unanswered_question(request, current_task):
    """
    Retrieves the next unanswered question for the user in the given task.
    Returns None if all questions have been answered.
    """
    unanswered_questions = (
        Question.objects.filter(task=current_task)
        .exclude(answer__user=request.user)
        .order_by("pk")
    )

    if unanswered_questions:
        return unanswered_questions.first()
    else:
        return None


@login_required
def question_detail(request, slug):
    """
    Displays a question and handles answer submissions.
    Redirects to the next unanswered question or a thank-you page when finished.
    """
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
    context = {}

    if sub_questions.exists():
        # Handle SubQuestion logic
        if request.method == "POST":
            valid_answers = []  # Collect valid answers here
            unanswered_sub_questions = []

            for sub_question in sub_questions:
                has_choices = sub_question.choice_set.exists()

                # Check for submitted data
                choice_id = request.POST.get(str(sub_question.id), None)
                print("before forced choice:", choice_id)

                notes = request.POST.get(f"notes_{sub_question.id}", "")
                print(notes)
                if choice_id is None:
                    # Assign a dummy choice if the subquestion has no choices
                    dummy_choice, created = Choice.objects.get_or_create(
                        question=sub_question.question,
                        sub_question=sub_question,
                        choice_text="Comments",
                    )
                    choice_id = dummy_choice.id

                form_data = {"choice": choice_id, "notes": notes}
                print(choice_id, form_data)
                form = AnswerForm(form_data)
                form.fields["choice"].queryset = sub_question.choice_set.all()

                if form.is_valid():
                    answer = form.save(commit=False)
                    answer.reaction_time = request.POST.get("reaction_time", None)
                    answer.delay_time = request.POST.get("delay_time", None)
                    answer.task = task
                    answer.question = question
                    answer.sub_question = sub_question
                    answer.user = request.user
                    valid_answers.append(answer)
                else:
                    unanswered_sub_questions.append(sub_question)

            if len(valid_answers) == sub_questions.count():
                for answer in valid_answers:
                    answer.save()

                next_question = get_next_unanswered_question(request, task)
                if next_question:
                    return redirect(
                        "retimgeval:question_detail", slug=next_question.slug
                    )
                else:
                    return redirect("retimgeval:thank_you", alias=task.alias)
            else:
                context["unanswered_sub_questions"] = unanswered_sub_questions

        sub_questions_and_forms = []
        for sub_question in sub_questions:
            form = AnswerForm()
            form.fields["choice"].queryset = sub_question.choice_set.all()
            sub_questions_and_forms.append((sub_question, form))

        context.update(
            {
                "question": question,
                "sub_questions_and_forms": sub_questions_and_forms,
                "reaction_time": request.GET.get("reaction_time", None),
                "delay_time": request.GET.get("delay_time", None),
            }
        )

    else:
        # Handle original Question logic
        choices = question.choice_set.all()
        if request.method == "POST":
            form = AnswerForm(request.POST)
            form.fields["choice"].queryset = choices

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
                    return redirect(
                        "retimgeval:question_detail", slug=next_question.slug
                    )
                else:
                    return redirect("retimgeval:thank_you", alias=task.alias)
        else:
            form = AnswerForm()
            form.fields["choice"].queryset = choices

        context.update(
            {
                "question": question,
                "choices": choices,
                "form": form,
                "reaction_time": request.GET.get("reaction_time", None),
                "delay_time": request.GET.get("delay_time", None),
            }
        )
    if task.alias == "erm-macula":
        return render(request, "retimgeval/question_detail_macula.html", context)
    else:
        return render(request, "retimgeval/question_detail.html", context)


class ThankYouPageView(View):
    """
    Displays a thank-you page after the user completes all questions in a task.
    """
    def get(self, request, alias):
        """
        Handles GET request to show the thank-you page and suggest the next task.
        """
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
