from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Question, Answer


# Create your views here.


@login_required
def menu(request):
    if request.path == '/accounts/logout/':
        logout(request)
        return redirect(settings.LOGIN_URL, request.path)
    else:
        return render(request, 'math_puzzle/menu.html')


@login_required
def instruction(request):
    if request.path == '/accounts/logout/':
        logout(request)
        return redirect(settings.LOGIN_URL, request.path)
    else:
        return render(request, 'math_puzzle/instruction.html')


@login_required
def game(request):
    if request.path == '/accounts/logout/':
        logout(request)
        return redirect(settings.LOGIN_URL, request.path)
    else:
        return render(request, 'math_puzzle' + request.path[0: -1] + '.html')


class TestView(ListView):
    template_name = 'math_puzzle/test.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Question.objects.order_by('-date_published')[:2]

