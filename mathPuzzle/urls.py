from django.conf.urls import url

from mathPuzzle import views

urlpatterns = [
    url(r'^$', views.menu, name='menu'),
    url(r'^lvl1/', views.game, name='lvl1'),
    url(r'^lvl2/', views.game, name='lvl2'),
    url(r'^lvl3/', views.game, name='lvl3'),
    url(r'^lvl4/', views.game, name='lvl4'),
    url(r'^instruction', views.instruction, name='instruction'),
    url(r'accounts/logout/', views.logout, name='logout'),
    url(r'accounts/register/', views.CreateUserFormView.as_view(), name='register'),
    url(r'accounts/profile/', views.profile, name='profile'),
    url(r'accounts/verification/', views.VerificationFormView.as_view(), name='verification'),
    url(r'accounts/activate', views.check_token, name='activate_token'),
    url(r'accounts/(?P<user_id>\d+)/send_email', views.send_activate_email, name='email_verification'),
    url(r'loto_menu/$', views.loto_menu, name="loto_menu"),
    url(r'^task/$', views.test, name='task'),
    url(r'^task/(?P<task_id>\d+)/question/(?P<question_number>\d+)/$', views.show_question, name='show_question'),
    url(r'^result/(?P<task_result_id>\d+)/$', views.result, name='result'),
    url(r'^crossword', views.crossword, name='crossword'),
    url(r'^api/school_classes/(?P<school_id>\d+)', views.get_school_classes, name='school_classes')
    # url(r'^task/(?P<task_id>\d+)/question/(?P<question_number>\d+)/$', views.detail, name='detail'),
    # url(r'^task/(?P<task_id>\d+)/question/(?P<question_number>\d+)/answer/$', views.answer, name='answer'),
]
