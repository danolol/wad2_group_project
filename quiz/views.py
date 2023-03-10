from django.shortcuts import render, redirect
from quiz.models import Quiz, Question, Answer
from quiz.models import Outcome
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

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

def take_quiz(request, quiz_title_slug):
    context_dict = {}

    quiz = Quiz.objects.get(slug=quiz_title_slug)
    
    context_dict['quiz'] = quiz
    return render(request, 'quiz/take_quiz.html', context=context_dict)

def quiz_result(request, quiz_title_slug):
    selected_array = [0, 0, 0, 0]
    
    quiz = Quiz.objects.get(slug=quiz_title_slug)

    if request.method == 'POST':
        questions = quiz.question_set.all()

        for question in questions:
            selected_answer = question.answer_set.get(pk=request.POST[f'answer{question.id}'])
            selected_array[selected_answer.index] += 1

    
    max = 0
    for i in range(len(selected_array)):
        if max < selected_array[i]:
            most_common_index = i
            max = selected_array[i]
            
    final_outcome = None
    outcomes = Outcome.objects.filter(quiz_id = quiz.id)
    for outcome in outcomes:
        if outcome.index == most_common_index:
            final_outcome = outcome
            break
    
    context_dict = {}
    context_dict['outcome'] = final_outcome
    context_dict['quiz'] = quiz
    
    print(context_dict['quiz'])
    print(context_dict['outcome'])
    return render(request, 'quiz/result.html', context=context_dict)

    


    