import json

from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, View

from .forms import AnnotationForm, ConsentForm
from .models import Annotation, Consent, Image


class LandingPageView(CreateView):
    model = Consent
    form_class = ConsentForm
    template_name = "retimgann/landing_page.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user has already given consent
            user_consent = Consent.objects.filter(
                user=request.user, consented=True
            ).first()
            if user_consent:
                # If user has given consent, redirect to the annotation page
                return redirect("retimgann:annotation_page", image_id=1)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect("retimgann:annotation_page", image_id=1)


def annotate(request, image_id):
    try:
        image = Image.objects.get(index=image_id)
        total_num_images = Image.objects.count()

        if request.method == "POST":
            # Annotation form submitted
            coordinates = json.loads(request.POST.get("coordinates"))
            time_spent = request.POST.get(
                "time_spent"
            )  # get the time_spent value from the form
            mouse_trajectory = json.loads(request.POST.get("mouse_trajectory"))
            annotation, created = Annotation.objects.get_or_create(
                user=request.user,
                image=image,
                defaults={
                    "coordinates": json.dumps(coordinates),
                    "time_spent": time_spent,
                    "mouse_trajectory": json.dumps(mouse_trajectory),
                },
            )
            if not created:
                # if the annotation already exists, update the coordinates
                annotation.coordinates = json.dumps(coordinates)
                annotation.time_spent = time_spent  # update time_spent
                annotation.mouse_trajectory = json.dumps(mouse_trajectory)
                annotation.save()
            return redirect("retimgann:annotation_page", image_id=image_id + 1)
    except ObjectDoesNotExist:
        return redirect("retimgann:thank_you")

    annotation = Annotation.objects.filter(user=request.user, image=image).first()

    if annotation:
        existing_annotation = mark_safe(json.dumps(json.loads(annotation.coordinates)))
        existing_time_spent = annotation.time_spent
        existing_mouse_trajectory = mark_safe(
            json.dumps(json.loads(annotation.mouse_trajectory))
        )
    else:
        existing_annotation = []
        existing_time_spent = 0
        existing_mouse_trajectory = []

    return render(
        request,
        "retimgann/annotation_page.html",
        {
            "image": image,
            "total_num_images": total_num_images,
            "existing_annotation": existing_annotation,
            "existing_time_spent": existing_time_spent,
            "existing_mouse_trajectory": existing_mouse_trajectory,
        },
    )


def annotate_submit(request):
    if request.method == "POST":
        # Annotation form submitted
        coordinates = json.loads(request.POST.get("coordinates"))
        time_spent = request.POST.get(
            "time_spent"
        )  # get the time_spent value from the form
        mouse_trajectory = json.loads(request.POST.get("mouse_trajectory"))

        image_id = request.POST.get("image_id")
        image = Image.objects.get(index=image_id)
        annotation, created = Annotation.objects.get_or_create(
            user=request.user,
            image=image,
            defaults={
                "coordinates": json.dumps(coordinates),
                "time_spent": time_spent,
                "mouse_trajectory": json.dumps(mouse_trajectory),
            },
        )
        if not created:
            # if the annotation already exists, update the coordinates and time_spent
            annotation.coordinates = json.dumps(coordinates)
            annotation.time_spent = time_spent  # update time_spent
            annotation.mouse_trajectory = json.dumps(mouse_trajectory)
            annotation.save()
        try:
            return redirect("retimgann:annotation_page", image_id=image_id + 1)
        except ObjectDoesNotExist:
            return redirect("retimgann:thank_you")

    # Should not reach here
    return redirect("home")


def thank_you(request):
    return render(request, "retimgann/thank_you.html")
