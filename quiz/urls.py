from django.urls import path
from . import views



app_name = 'quiz'


urlpatterns = [
    path('', views.home, name='home'),
    path('makequiz/pre/', views.pre_make_quiz, name='pre_make_quiz'),
    path('makequiz/<num_questions>/<num_outcomes>/', views.make_quiz_main, name='make_quiz_main'),
    path('makequiz/thanks', views.make_quiz_result, name='make_quiz_result'),
    path('quizzes/', views.show_quizzes, name = 'show_quizzes'),
    path('quizzes/<slug:quiz_title_slug>/', views.take_quiz, name = 'take_quiz'),
    path('quizzes/<slug:quiz_title_slug>/result', views.quiz_result, name = 'quiz_result'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>', views.ProfileView.as_view(), name='profile'),
    path('profile/update_user/', views.update_user, name='update_user'),
]
