from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas


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

