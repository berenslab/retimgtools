from csvexport.actions import csvexport
from django.contrib import admin

from .models import Annotation, Consent, Image, Task


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["user", "consented", "consented_at"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["task", "index", "image", "name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "category",
        "is_active",
        "created_at",
        "updated_at",
        "alias",
    ]


class AnnotationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "image",
        "coordinates",
        "mouse_trajectory_summary",  # use the summary method instead of the raw field
        "time_spent",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "user",
    ]

    def mouse_trajectory_summary(self, obj):
        last_positions = obj.mouse_trajectory[-200:]
        # Convert the positions to strings and join them with commas
        return last_positions

    mouse_trajectory_summary.short_description = (
        "Mouse Trajectory"  # set the column header
    )

    actions = [csvexport]

    list_per_page = 5000


admin.site.register(Annotation, AnnotationAdmin)
