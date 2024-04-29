from csvexport.actions import csvexport
from django.contrib import admin

from .models import Answer, Choice, Consent, Question, SubQuestion, Task


# Register your models here.
@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["user", "task", "consented", "consented_at"]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "sub_question", "created_at")
    list_filter = ("sub_question", "created_at")
    search_fields = ("choice_text", "question", "subquestion")


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "choice",
        "user",
        "task",
        "question",
        "sub_question",
        "answered_at",
        "reaction_time",
        "delay_time",
    )
    list_filter = ("user", "task")
    search_fields = ("choice", "user")

    actions = [csvexport]

    list_per_page = 1000


class TaskAdmin(admin.ModelAdmin):
    list_display = ("category", "alias", "description", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("description", "category")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("description", "task", "created_at")
    list_filter = ("task", "created_at")
    search_fields = ("description", "task")

    inlines = [ChoiceInline]


class SubQuestionAdmin(admin.ModelAdmin):
    list_display = ("description", "question", "created_at")
    list_filter = ("question", "created_at")
    search_fields = ("description", "question")

    inlines = [ChoiceInline]


admin.site.register(Task, TaskAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SubQuestion, SubQuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
