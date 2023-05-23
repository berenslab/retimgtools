from django.shortcuts import render

from retimgeval.models import Task


def home(request):
    tasks = Task.objects.all()
    return render(request, "pages/home.html", {"tasks": tasks})
