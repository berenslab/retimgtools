from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "retimgeval"
urlpatterns = [
    path(
        "<str:alias>/instruction/",
        views.TaskInstructionView.as_view(),
        name="task_instruction",
    ),
    path(
        "<str:slug>",
        views.question_detail,
        name="question_detail",
    ),
    path("<str:alias>/thanks/", views.ThankYouPageView.as_view(), name="thank_you"),
]
