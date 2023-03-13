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
from quiz.forms import QuizForm, OutcomeForm, QuestionForm, AnswerForm
import datetime


def home(request):
    context_dict = {}

    response = render(request, 'quiz/home.html', context=context_dict)
    return response

def pre_make_quiz(request):
    context_dict = {}
    context_dict['questions_message'] = "Please enter a number of questions for your quiz: "
    context_dict['outcomes_message'] = """Please enter a number of outcomes for your quiz (bare in mind 
    each question must have an equal number of outcomes): """

    if request.method == "POST":
        num_questions = request.POST['questions']
        num_outcomes = request.POST['outcomes']
        return redirect(reverse('quiz:make_quiz_main', kwargs={'num_questions':num_questions, 'num_outcomes':num_outcomes}))

    return render(request, 'quiz/pre_make_quiz.html', context=context_dict)

def make_quiz_main(request, num_questions, num_outcomes):
    num_questions = int(num_questions)
    num_outcomes = int(num_outcomes)

    quiz_form = QuizForm(prefix = 'quiz')
    OutcomesFormset = formset_factory(OutcomeForm, extra=num_outcomes)
    QuestionsFormset = formset_factory(QuestionForm, extra=num_questions)
    AnswersFormset = formset_factory(AnswerForm, extra=num_outcomes*num_questions)
    
    outcomes_formset = OutcomesFormset(prefix = 'outcome')
    questions_formset = QuestionsFormset(prefix = 'question')
    answers_formset = AnswersFormset(prefix = 'answer')

    context_dict = {}
    context_dict['quiz_form'] = quiz_form
    context_dict['outcomes_formset'] = outcomes_formset
    context_dict['questions_formset'] = questions_formset
    context_dict['answers_formset'] = answers_formset
    context_dict['num_questions'] = num_questions
    context_dict['num_outcomes'] = num_outcomes

    ##Handle response & validate forms
    if request.method == "POST":
        quiz_form = QuizForm(request.POST, prefix='quiz')

        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
        
        else:
            print(quiz_form.errors)

        for i in range(num_outcomes):
            outcome_form = OutcomeForm(request.POST, prefix=f'outcome-{i}')
            if outcome_form.is_valid():
                outcome = outcome_form.save(commit=False)
                outcome.quiz_id = quiz.id
                outcome.index= i
                outcome.save()
        
            else:
                print(outcome_form.errors)
                

        counter = 0
        for i in range(num_questions):
            question_form = QuestionForm(request.POST, prefix=f'question-{i}')
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.quiz_id = quiz.id
                question.save()
            
            else:
                print(question_form.errors)
            
            for j in range(num_outcomes):
                answer_form = AnswerForm(request.POST, prefix=f'answer-{counter}')
                print(answer_form)
                if answer_form.is_valid():
                    answer = answer_form.save(commit=False)
                    answer.question_id = question.id
                    answer.index = j
                    answer.save()
                    counter += 1
                
                else:
                    print(answer_form.errors)
        
        return render(request, 'quiz/make_quiz_result.html')

    return render(request, 'quiz/make_quiz.html', context=context_dict)

def make_quiz_result(request, num_questions, num_outcomes):

    num_questions, num_outcomes = int(num_questions), int(num_outcomes)
    quiz_form = QuizForm(request.POST, prefix='quiz')

    if quiz_form.is_valid():
        quiz = quiz_form.save(commit=False)
        quiz.creator = request.user
        quiz.save()
    
    else:
        print(quiz_form.errors)

    for i in range(num_outcomes):
        outcome_form = OutcomeForm(request.POST, prefix=f'outcome-{i}')
        if outcome_form.is_valid():
            outcome = outcome_form.save(commit=False)
            outcome.quiz_id = quiz.id
            outcome.index= i
            outcome.save()
    
        else:
            print(outcome_form.errors)
            

    counter = 0
    for i in range(num_questions):
        question_form = QuestionForm(request.POST, prefix=f'question-{i}')
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz_id = quiz.id
            question.save()
        
        else:
            print(question_form.errors)
        
        for j in range(num_outcomes):
            answer_form = AnswerForm(request.POST, prefix=f'answer-{counter}')
            print(answer_form)
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.question_id = question.id
                answer.index = j
                answer.save()
                counter += 1
            
            else:
                print(answer_form.errors)
    
    return render(request, 'quiz/make_quiz_result.html')

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
