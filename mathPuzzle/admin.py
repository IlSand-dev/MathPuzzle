from django.contrib import admin

# Register your models here
from .models import Question, Answer, Task


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)

admin.site.register(Task)
