from django.urls import path
from quiz import views


app_name = 'quiz'


urlpatterns = [
    path('', views.home, name='home'),
    path('makequiz/', views.make_quiz, name='make_quiz'),
    path('quizzes/', views.show_quizzes, name = 'show_quizzes'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
]
