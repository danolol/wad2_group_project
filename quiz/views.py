from quiz.models import Quiz, Question, Answer, Outcome
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse, get_object_or_404
from quiz.models import UserProfile
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from members.forms import ProfilePicForm, RegisterUserForm
from quiz.forms import QuizForm, OutcomeForm, QuestionForm, AnswerForm
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone


def home(request):
    context_dict = {}

    most_viewed = Quiz.objects.order_by('-views')[:5]
    most_recent = Quiz.objects.filter(date__lte=timezone.now()).order_by('-date')[:5]
    context_dict['views'] = most_viewed
    context_dict['recents'] = most_recent

    response = render(request, 'quiz/home.html', context=context_dict)
    return response

@login_required
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

@login_required
def make_quiz_main(request, num_questions, num_outcomes):
    num_questions = int(num_questions)
    num_outcomes = int(num_outcomes)

    ## Create all required forms for quiz, outcome, question & answer entities
    quiz_form = QuizForm(prefix = 'quiz')
    OutcomesFormset = formset_factory(OutcomeForm, min_num = num_outcomes, max_num=num_outcomes)
    QuestionsFormset = formset_factory(QuestionForm, min_num=num_questions, max_num=num_questions)
    AnswersFormset = formset_factory(AnswerForm, min_num=num_outcomes*num_questions, max_num = num_outcomes*num_questions)
    
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
    context_dict['errors'] = None
    context_dict['not_unique'] = False

    ## Handle response & validate forms
    if request.method == "POST":

        ##print(request.FILES)

        quiz_form = QuizForm(request.POST, prefix='quiz')
        outcomes_formset = OutcomesFormset(request.POST, request.FILES, prefix='outcome')
        questions_formset = QuestionsFormset(request.POST, prefix='question')
        answers_formset = AnswersFormset(request.POST, prefix='answer')

        ## If input is valid...
        if quiz_form.is_valid() and outcomes_formset.is_valid() and questions_formset.is_valid() and answers_formset.is_valid():
            
            ## Guarantee uniqueness
            try: 
                quiz = quiz_form.save(commit=False)
                quiz.creator = get_object_or_404(UserProfile, user=request.user)
                quiz.save()
            except IntegrityError:
                context_dict['not_unique'] = True
                return render(request, 'quiz/make_quiz.html', context=context_dict)

        ## Process all forms sequentially
            for i in range(num_outcomes):
                outcome_form = OutcomeForm(request.POST, request.FILES, prefix=f'outcome-{i}')
                outcome = outcome_form.save(commit=False)
                outcome.index= i
                outcome.quiz_id = quiz.id
                outcome.save()

            counter = 0
            for i in range(num_questions):
                question_form = QuestionForm(request.POST, prefix=f'question-{i}')
                question = question_form.save(commit=False)
                question.quiz_id = quiz.id
                question.save()

                for j in range(num_outcomes):
                    answer_form = AnswerForm(request.POST, prefix=f'answer-{counter}')
                    answer = answer_form.save(commit=False)
                    answer.question_id = question.id
                    answer.index = j
                    answer.save()
                    counter += 1

            return render(request, 'quiz/make_quiz_result.html')
        
        ## If input is invalid, pass errors into form and rerender with saved user input
        else:
            errors = True
            context_dict['errors'] = errors
            context_dict['quiz_form'] = quiz_form
            context_dict['outcomes_formset'] = outcomes_formset
            context_dict['questions_formset'] = questions_formset
            context_dict['answers_formset'] = answers_formset
            
    return render(request, 'quiz/make_quiz.html', context=context_dict)

@login_required
def make_quiz_result(request):
    return render(request, 'quiz/make_quiz_result.html')

def show_quizzes(request):
    top_viewed = Quiz.objects.order_by('-views')[:20]
    recently_added =  Quiz.objects.order_by('-date')

    context_dict = {}
    context_dict['top_viewed'] = top_viewed
    context_dict['recently_added'] = recently_added
    
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

class ProfileView(View):

    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = ProfilePicForm({'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('quiz:home'))

        context_dict = {'user_profile': user_profile, 
                        'selected_user': user, 
                        'form': form}
        
        return render(request, 'quiz/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('quiz:home'))
        form = ProfilePicForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('quiz:profile', username=request.user.username)
        else:
            print(form.errors)
            context_dict = {'user_profile': user_profile, 
                            'selected_user': user, 
                            'form': form}
            
            return render(request, 'quiz/profile.html', context_dict)
        

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = UserProfile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = RegisterUserForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "quiz/update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        quizzes = Quiz.objects.filter(title__contains=searched)

        return render(request, 'quiz/search_venues.html', {'searched': searched, 'quizzes': quizzes})
    else:
        return render(request, 'quiz/search_venues.html', {})