from django.contrib import admin

from .models import Annotation, Consent, Image


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["user", "consented"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "name"]


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ["user", "image", "coordinates"]
