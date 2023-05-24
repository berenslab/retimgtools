from csvexport.actions import csvexport
from django.contrib import admin

from .models import Annotation, Consent, Image


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["user", "consented", "consented_at"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["index", "image", "name"]


class AnnotationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "image",
        "coordinates",
        "time_spent",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "user",
    ]

    actions = [csvexport]


admin.site.register(Annotation, AnnotationAdmin)
