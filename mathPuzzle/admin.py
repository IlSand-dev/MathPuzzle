from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Question, Answer, Task, Role, School, SchoolClass


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class RoleInline(admin.StackedInline):
    model = Role
    can_delete = False


class RoleAdmin(UserAdmin):
    inlines = (RoleInline, )


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)

admin.site.register(Task)

admin.site.unregister(User)

admin.site.register(User, RoleAdmin)

admin.site.register(School)

admin.site.register(SchoolClass)
