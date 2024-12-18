from django.urls import path
from AbobaHelp import settings
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<tag>', views.found_questions, name="tag_questions"),
    path('question/<int:qid>', views.question_page, name="question_page"),
    path('question/<int:qid>/like/', views.like_question, name="like_question"),
    path('answer/<int:aid>/like/', views.like_answer, name="like_answer"),
    path('answer/<int:aid>/correct/', views.correct_answer, name="correct_answer"),
    path('profile/edit/', views.settings, name="settings"),
    path('ask/', views.ask, name="ask"),
    path(settings.LOGIN_URL[1:], views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
]
