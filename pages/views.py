from django.shortcuts import render

from retimgeval.models import Task


def home(request):
    tasks = Task.objects.all().order_by("created_at")
    return render(request, "pages/home.html", {"tasks": tasks})
