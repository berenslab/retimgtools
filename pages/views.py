from django.shortcuts import render

from retimgann.models import Task as AnnotationTask
from retimgeval.models import Task as EvaluationTask


def home(request):
    evalutation_tasks = EvaluationTask.objects.all().order_by("created_at")
    annotation_tasks = AnnotationTask.objects.all().order_by("created_at")
    return render(
        request,
        "pages/home.html",
        {"evalutation_tasks": evalutation_tasks, "annotation_tasks": annotation_tasks},
    )
