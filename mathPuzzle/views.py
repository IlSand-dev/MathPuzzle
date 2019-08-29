from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .models import Question, Answer, Task


# Create your views here.


@login_required
def logout(request):
    return logout_then_login(request)


@login_required
def menu(request):
    return render(request, 'math_puzzle/menu.html')


@login_required
def instruction(request):
    return render(request, 'math_puzzle/instruction.html')


@login_required
def game(request):
    return render(request, 'math_puzzle' + request.path + '.html')


def test(request):
    return render(request, "math_puzzle/question.html", {"tasks_list": Task.objects.order_by('id')[:5]})


def detail(request, question_id):
    return render(request, "math_puzzle/answer.html", {"question": get_object_or_404(Question, pk=question_id)})


def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'math_puzzle/answer.html',
                      {'question': question, 'error_message': 'Answer does not exist'})
    if answer.is_right:
        if int(question_id) != Question.objects.latest('id').id:
            return redirect("/question/" + str(int(question_id) + 1))
        else:
            return redirect("/question/")
    else:
        return render(request, 'math_puzzle/answer.html', {'question': question, 'error_message': 'Wrong Answer!'})
