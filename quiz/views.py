from django.shortcuts import render

def home(request):
    context_dict = {}

    response = render(request, 'quiz/home.html', context=context_dict)
    return response

def make_quiz(request):
    context_dict = {}

    response = render(request, 'quiz/make_quiz.html', context=context_dict)
    return response

def show_quizzes(request):
    context_dict = {}
    
    response = render(request, 'quiz/show_quizzes.html', context=context_dict)
    return response