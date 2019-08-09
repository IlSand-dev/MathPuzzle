from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render, redirect


# Create your views here.


def game(request):
    if request.path == '/accounts/logout/':
        logout(request)
        return redirect(settings.LOGIN_URL, request.path)
    else:
        if request.user.is_authenticated:
            return render(request, 'math_puzzle/game.html')
        else:
            return redirect(settings.LOGIN_URL, request.path)
