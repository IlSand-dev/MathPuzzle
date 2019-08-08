from django.urls import path

from mathPuzzle import views

urlpatterns = [
    path('', views.game, name='game'),
]