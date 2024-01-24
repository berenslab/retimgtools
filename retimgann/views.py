import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, View

from .forms import AnnotationForm, ConsentForm
from .models import Annotation, Consent, Image, Task


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


def annotate(request, task_id, image_id):
    task = get_object_or_404(Task, id=task_id)  # Get the task
    images = Image.objects.filter(task=task).order_by(
        "index"
    )  # Get images for the task, ordered by index

    # Attempt to get the current image; redirect if it doesn't exist within the task
    try:
        image = images.get(index=image_id)
    except Image.DoesNotExist:
        return redirect("retimgann:thank_you")  # Or appropriate handling

    total_num_images = images.count()

    if request.method == "POST":
        # Annotation form submission logic remains the same
        coordinates = json.loads(request.POST.get("coordinates"))
        mouse_trajectory = json.loads(request.POST.get("mouse_trajectory"))
        time_spent = request.POST.get("time_spent")

        annotation, created = Annotation.objects.get_or_create(
            user=request.user,
            image=image,
            defaults={
                "coordinates": json.dumps(coordinates),
                "mouse_trajectory": json.dumps(mouse_trajectory),
                "time_spent": time_spent,
            },
        )
        if not created:
            annotation.coordinates = json.dumps(coordinates)
            annotation.mouse_trajectory = json.dumps(mouse_trajectory)
            annotation.time_spent = time_spent
            annotation.save()

        # Find the next image in the task to annotate
        next_image_index = image.index + 1
        if images.filter(index=next_image_index).exists():
            return redirect(
                "retimgann:annotate", task_id=task_id, image_id=next_image_index
            )
        else:
            return redirect("retimgann:thank_you")

    # Check if there's an existing annotation for this image
    annotation = Annotation.objects.filter(user=request.user, image=image).first()
    existing_annotation = mark_safe(
        json.dumps(annotation.coordinates if annotation else [])
    )
    existing_time_spent = annotation.time_spent if annotation else 0
    existing_mouse_trajectory = mark_safe(
        json.dumps(annotation.mouse_trajectory if annotation else [])
    )

    return render(
        request,
        "retimgann/annotation_page.html",
        {
            "image": image,
            "task": task,
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
        mouse_trajectory = json.loads(request.POST.get("mouse_trajectory"))
        time_spent = request.POST.get(
            "time_spent"
        )  # get the time_spent value from the form

        task_id = request.POST.get("task_id")
        image_id = request.POST.get("image_id")
        image = Image.objects.get(index=image_id)
        annotation, created = Annotation.objects.get_or_create(
            user=request.user,
            image=image,
            defaults={
                "coordinates": json.dumps(coordinates),
                "mouse_trajectory": json.dumps(mouse_trajectory),
                "time_spent": time_spent,
            },
        )
        if not created:
            # if the annotation already exists, update the coordinates and time_spent
            annotation.coordinates = json.dumps(coordinates)
            annotation.mouse_trajectory = json.dumps(mouse_trajectory)
            annotation.time_spent = time_spent  # update time_spent
            annotation.save()
        try:
            return redirect(
                "retimgann:annotate", task_id=task_id, image_id=image_id + 1
            )
        except ObjectDoesNotExist:
            return redirect("retimgann:thank_you")

    # Should not reach here
    return redirect("home")


def task_selection(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    first_image = Image.objects.filter(task=task).order_by("index").first()

    if first_image:
        # Redirect to the annotation page with the task_id and the first image's index
        return redirect(
            "retimgann:annotate", task_id=task.id, image_id=first_image.index
        )
    else:
        # Handle the case where there are no images for the task
        # Maybe redirect to a page that indicates this or shows an error message
        return render(request, "retimgann/thank_you.html")


def thank_you(request):
    return render(request, "retimgann/thank_you.html")
