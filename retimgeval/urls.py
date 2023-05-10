from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "retimgeval"
urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("tasks", views.task_list, name="task_list"),
    path(
        "tasks/<int:pk>/instruction/",
        views.TaskInstructionView.as_view(),
        name="task_instruction",
    ),
    path(
        "<str:slug>",
        views.question_detail,
        name="question_detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
