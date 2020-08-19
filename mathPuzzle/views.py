from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import FormView

from .forms import CreateUserForm
from .models import Question, Answer, Task, TaskResult, Role


# Create your views here.


@login_required
def logout(request):
    return logout_then_login(request)


@login_required
def menu(request):
    return render(request, 'math_puzzle/menu.html')


@login_required
def loto_menu(request):
    return render(request, "math_puzzle/loto_menu.html")


@login_required
def instruction(request):
    return render(request, 'math_puzzle/instruction.html')


@login_required
def game(request):
    return render(request, 'math_puzzle' + request.path[0:-1] + '.html')


@login_required
def crossword(request):
    return render(request, 'math_puzzle/crossword.html')


@login_required
def test(request):
    return render(request, "math_puzzle/question.html", {"tasks_list": Task.objects.order_by('id')[:5]})


@login_required
def show_question(request, task_id, question_number):
    task = get_object_or_404(Task, pk=task_id)
    question_number = int(question_number)
    question = task.question_set.get(number=question_number)

    task_result_id = request.POST.get('task_result_id')
    if task_result_id:
        task_result = get_object_or_404(TaskResult, id=task_result_id)
        if question_number == task_result.question_number:
            if question.type == 'multiply_answer' or question.type == 'single_answer':
                req_answer = set(map(int, request.POST.getlist('answer_id')))
                if req_answer:
                    right_answers = set([answer.id for answer in question.answer_set.filter(is_right=True)])
                    right = req_answer == right_answers
                    if right:
                        task_result.result += 1
                        task_result.save()
            elif question.type == 'open_answer':
                answer = request.POST.get('answer').lower()
                right_answer = list(question.answer_set.filter(is_right=True))[0].text.lower()
                if answer == right_answer:
                    task_result.result += 1
                    task_result.save()
            question_number += 1
            if question_number > task.question_set.latest('number').number:
                return redirect("/result/" + task_result_id)
            task_result.question_number += 1
            task_result.save()
            question = task.question_set.get(number=question_number)
        else:
            question_number = task_result.question_number
            question = task.question_set.get(number=question_number)
    else:
        task_result = TaskResult(user_id=request.user, task_id=task, question_number=question_number)
        task_result.save()
        task_result_id = task_result.id

    return render(request, "math_puzzle/answer.html",
                  {"question": question,
                   "task": task,
                   "task_result_id": task_result_id})


def result(request, task_result_id):
    return render(request, 'math_puzzle/results.html',
                  {'task_result': get_object_or_404(TaskResult, pk=task_result_id)})


def profile(request):
    user_role = request.user.role.role
    if str(user_role) == request.user.role.GUEST:
        return render(request, 'registration/profiles/guest_profile.html')
    elif str(user_role) == request.user.role.STUDENT:
        return render(request, 'registration/profiles/student_profile.html')
    elif str(user_role) == request.user.role.TEACHER:
        return render(request, 'registration/profiles/teacher_profile.html')


class CreateUserFormView(FormView):
    form_class = CreateUserForm
    success_url = '/'
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        user.role = Role()
        user.role.save()
        return super(CreateUserFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateUserFormView, self).form_invalid(form)
