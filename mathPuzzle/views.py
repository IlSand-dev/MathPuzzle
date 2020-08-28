import json
import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import FormView

from math_puzzle import settings
from .decorators import should_be_active
from .forms import CreateUserForm, VerificationForm
from .models import Task, TaskResult, Role, SchoolClass


# Create your views here.


@login_required
def logout(request):
    return logout_then_login(request)


@login_required
# @should_be_active
def menu(request):
    return render(request, 'math_puzzle/menu.html')


@login_required
# @should_be_active
def loto_menu(request):
    return render(request, "math_puzzle/loto_menu.html")


@login_required
# @should_be_active
def instruction(request):
    return render(request, 'math_puzzle/instruction.html')


@login_required
# @should_be_active
def game(request):
    return render(request, 'math_puzzle' + request.path[0:-1] + '.html')


@login_required
# @should_be_active
def crossword(request):
    return render(request, 'math_puzzle/crossword.html')


@login_required
# @should_be_active
def test(request):
    return render(request, "math_puzzle/question.html", {"tasks_list": Task.objects.order_by('id')[:5]})


@login_required
# @should_be_active
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


@login_required
@should_be_active
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
    success_url = '/accounts/send_email'
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        user.role = Role()
        user.role.save()
        self.success_url = '/accounts/' + str(user.id) + '/activate_token'
        return super(CreateUserFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateUserFormView, self).form_invalid(form)


class VerificationFormView(FormView):
    form_class = VerificationForm
    success_url = 'accounts/profile/'
    template_name = 'registration/verification.html'

    def form_valid(self, form):
        verification_data = form.cleaned_data
        current_user = self.request.user
        current_user.first_name = verification_data['first_name']
        current_user.last_name = verification_data['last_name']
        school_class = [get_object_or_404(SchoolClass, id=verification_data['school_class'])]
        current_user.role.school_class.set(school_class)
        current_user.role.role = current_user.role.STUDENT
        current_user.save()
        current_user.role.save()
        return super(VerificationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(VerificationFormView, self).form_invalid(form)


def get_school_classes(request, school_id):
    response = {'answer': []}
    for school_class in SchoolClass.objects.values():
        if school_class['school_id'] == int(school_id):
            response['answer'].append([school_class['id'], school_class['name']])
    new_response = json.dumps(response)
    return HttpResponse(new_response, content_type='application/json')


def send_activate_email(request, user_id):
    activate_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
    user = User.objects.get(id=user_id)
    user.role.activate_token = activate_token
    user.role.save()
    send_mail('Подтверждение email',
              'Для подтверждения почты перейдите по ссылке ' + request.build_absolute_uri(
                  '/accounts/activate/') + '?activate_token=' + activate_token,
              settings.EMAIL_HOST_USER,
              [user.email])
    return render(request, 'registration/email_verification.html')


def check_token(request):
    activate_token = request.GET.get("activate_token", "")
    users = list(User.objects.filter(role__activate_token=activate_token))
    for user in users:
        user.role.is_active = True
        user.role.save()
    return redirect('/')
