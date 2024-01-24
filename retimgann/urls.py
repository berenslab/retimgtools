from django.urls import path

from . import views

app_name = "retimgann"

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("task/<int:task_id>/<int:image_id>", views.annotate, name="annotate"),
    path("annotate_submit/", views.annotate_submit, name="annotate_submit"),
    path("thank_you/", views.thank_you, name="thank_you"),
    path("task/<int:task_id>/", views.task_selection, name="task_selection"),
]
