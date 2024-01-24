from django.urls import path

from . import views

app_name = "retimgann"

urlpatterns = [
    path("task/<int:task_id>/<int:image_id>", views.annotate, name="annotate"),
    path("annotate_submit/", views.annotate_submit, name="annotate_submit"),
    path("thank_you/", views.thank_you, name="thank_you"),
    path("task/<int:task_id>/", views.task_selection, name="task_selection"),
    path(
        "task/<int:task_id>/instruction/",
        views.task_instruction,
        name="task_instruction",
    ),
]
