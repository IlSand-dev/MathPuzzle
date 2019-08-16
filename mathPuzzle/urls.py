from django.urls import path

from mathPuzzle import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('lvl1/', views.game, name='lvl1'),
    path('lvl2/', views.game, name='lvl2'),
    path('lvl3/', views.game, name='lvl3'),
]