from django.conf.urls import url

from mathPuzzle import views


urlpatterns = [
    url(r'^$', views.menu, name='menu'),
    url(r'^lvl1', views.game, name='lvl1'),
    url(r'^lvl2', views.game, name='lvl2'),
    url(r'^lvl3', views.game, name='lvl3'),
    url(r'^lvl4', views.game, name='lvl4'),
    url(r'^instruction', views.instruction, name='instruction'),
    url(r'accounts/logout/', views.logout, name='logout'),
    url(r'^question/$', views.test, name='question'),
    url(r'^question/(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^question/(?P<question_id>\d+)/answer/$', views.answer, name='answer')
]