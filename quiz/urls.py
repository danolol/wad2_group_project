from django.urls import path
from quiz import views


app_name = 'quiz'


urlpatterns = [
    path('', views.home, name='home'),
    path('makequiz/', views.make_quiz, name='make_quiz'),
    path('quizzes/', views.show_quizzes, name = 'show_quizzes'),
    path('quizzes/<slug:quiz_title_slug>/', 
    views.take_quiz, name = 'take_quiz'),
    path('quizzes/<slug:quiz_title_slug>/result', views.quiz_result, name = 'quiz_result'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
]
