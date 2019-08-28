from django.urls import path

from mathPuzzle import views
from mathPuzzle.views import TestView

urlpatterns = [
    path('', views.menu, name='menu'),
    path('lvl1/', views.game, name='lvl1'),
    path('lvl2/', views.game, name='lvl2'),
    path('lvl3/', views.game, name='lvl3'),
    path('lvl4/', views.game, name='lvl4'),
    path('instruction', views.instruction, name='instruction'),
    path(r'test/', TestView.as_view(), name='test')
]