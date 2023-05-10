import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, View

from .forms import AnnotationForm, ConsentForm
from .models import Annotation, Consent, Image


class LandingPageView(CreateView):
    model = Consent
    form_class = ConsentForm
    template_name = "retimgann/landing_page.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(
            "retimgann:annotation_page", image_id=str(Image.objects.first().pk)
        )


def annotate(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
        total_num_images = Image.objects.count()
        if request.method == "POST":
            # Annotation form submitted
            coordinates = request.POST.get("coordinates")
            annotation = Annotation(
                user=request.user, image=image, coordinates=coordinates
            )
            annotation.save()
            return redirect("retimgann:annotation_page", image_id=image_id + 1)
    except:
        return redirect("retimgann:thank_you")

    # Render the annotation form
    return render(
        request,
        "retimgann/annotation_page.html",
        {"image": image, "total_num_images": total_num_images},
    )


def annotate_submit(request):
    if request.method == "POST":
        # Annotation form submitted
        coordinates = request.POST.get("coordinates")
        image_id = request.POST.get("image_id")
        image = Image.objects.get(id=image_id)
        annotation = Annotation(user=request.user, image=image, coordinates=coordinates)
        annotation.save()
        try:
            return redirect("retimgann:annotation_page", image_id=image_id + 1)
        except:
            return redirect("retimgann:thank_you")

    # Should not reach here
    return redirect("home")


def thank_you(request):
    return render(request, "retimgann/thank_you.html")
