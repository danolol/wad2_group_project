from quiz.models import Quiz, Question, Answer
from quiz.models import Outcome
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from .models import UserProfile
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from .forms import UserProfileForm


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

    


    
@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('quiz:home'))
        else:
            print(form.errors)

    context_dict = {'form': form}
    response = render(request, 'quiz/profile_registration.html', context_dict)
    return response


class ProfileView(View):

    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('quiz:home'))
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
        return render(request, 'quiz/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('quiz:home'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('quiz:profile', user.username)
        else:
            print(form.errors)
            context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
            return render(request, 'quiz/profile.html', context_dict)
