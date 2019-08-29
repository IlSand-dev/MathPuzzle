from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .models import Question, Answer, Task, TaskResult


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
            reqAnswer = request.POST.get('answer_id')
            print('reqAnswer:', reqAnswer)
            if reqAnswer:
                reqAnswer = int(reqAnswer)
                answer = question.answer_set.get(pk=reqAnswer)
                if answer.is_right:
                    task_result.result += 1
                    task_result.save()

            question_number += 1
            if question_number > task.question_set.latest('number').number:
                return redirect(f"/result/{task_result_id}")
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

# def detail(request, task_id, question_number):
#     task = get_object_or_404(Task, pk=task_id)
#     question_number = int(question_number) + 1
#     task_result_id = request.POST.get('task_result_id')
#     print('detail() task_result_id: ', task_result_id)
#     if task_result_id is None:
#         task_result = TaskResult(user_id=request.user, task_id=task)
#         task_result.save()
#         task_result_id = task_result.id
#         return render(request, "math_puzzle/answer.html",
#                       {"question": task.question_set.get(number=question_number),
#                        "task": task,
#                        "task_result_id": task_result_id})
#     else:
#         task_result = get_object_or_404(TaskResult, id=task_result_id)
#     print('task_result.result:', task_result.result)
#     if question_number > task.question_set.latest('number').number:
#         print(task_result.result)
#         return redirect("/task/")
#     question = task.question_set.get(number=question_number)
#     answer = question.answer_set.get(pk=request.POST['answer'])
#     if answer.is_right:
#         task_result.result += 1
#         task_result.save()
#     return render(request, "math_puzzle/answer.html",
#                   {"question": question,
#                    "task": task,
#                    "task_result_id": task_result_id})

# def answer(request, task_id, question_number):
#     task = get_object_or_404(Task, pk=task_id)
#     question = task.question_set.get(number=question_number)
#     task_result_id = request.POST.get('task_result_id')
#     print('answer() task_result_id: ', task_result_id)
#     task_result = get_object_or_404(TaskResult, pk=task_result_id)
#     try:
#         answer = question.answer_set.get(pk=request.POST['answer'])
#     except (KeyError, Answer.DoesNotExist):
#         return render(request, 'math_puzzle/answer.html',
#                       {'question': question, 'error_message': 'Answer does not exist'})
#     if answer.is_right:
#         task_result.result += 1
#         task_result.save()
#     if int(question_number) != task.question_set.latest('number').number:
#         return redirect(f'/task/{task_id}/question/{question_number}/')
#     else:
#         print(task_result.result)
#         return redirect("/task/")
