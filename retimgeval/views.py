from django.shortcuts import redirect, render
from django.views.generic import CreateView, View

from .forms import AnswerForm, ConsentForm
from .models import Choice, Consent, Question, Task


class LandingPageView(CreateView):
    model = Consent
    form_class = ConsentForm
    template_name = "retimgeval/landing_page.html"

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


def question_detail(request, slug):
    question = Question.objects.get(slug=slug)
    task = Task.objects.get(pk=question.task.pk)
    choices = question.choice_set.all()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        form.question = question
        form.fields["choice"].queryset = Choice.objects.filter(
            question_id=form.question.pk
        )

        option = None
        if form.is_valid():
            option = form.save(commit=False)
            option.reaction_time = request.POST.get("reaction_time", None)
            option.task = task
            option.question = question
            option.user = request.user
            option.save()
            try:
                # if task.pk != 1 and question.slug[-1] == "1":
                if question.task.id != 1 and question.slug[-1] == "1":
                    new_slug = slug[:-1] + "2"
                    Question.objects.get(slug=new_slug)
                    return redirect("retimgeval:question_detail", slug=new_slug)
                else:
                    new_slug = slug[:-3] + f"{int(slug[-3])+1}p1"
                    Question.objects.get(slug=new_slug)
                    return redirect(
                        "retimgeval:question_detail",
                        slug=new_slug,
                    )
            except:
                return redirect("retimgeval:task_list")
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
