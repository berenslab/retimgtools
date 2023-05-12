from csvexport.actions import csvexport
from django.contrib import admin

from .models import Answer, Choice, Consent, Question, Task


# Register your models here.
@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["user", "consented", "consented_at"]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "created_at")
    list_filter = ("question", "created_at")
    search_fields = ("choice_text", "question")


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "choice",
        "user",
        "task",
        "question",
        "answered_at",
        "reaction_time",
    )
    list_filter = ("user", "answered_at")
    search_fields = ("choice", "user")

    actions = [csvexport]


admin.site.register(Task)
admin.site.register(Question)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
