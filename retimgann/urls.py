from django.urls import path

from . import views

app_name = "retimgann"

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("<int:image_id>/", views.annotate, name="annotation_page"),
    path("annotate_submit/", views.annotate_submit, name="annotate_submit"),
    path("thank_you/", views.thank_you, name="thank_you"),
]
