import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'wad2_group_project.settings')
import django
django.setup()
from quiz.models import UserProfile, Quiz, Question, Answer, Review, Outcome
from django.contrib.auth.models import User
import datetime

def populate():

    programming_reviews = [
        {'user': 'Kazzoe',
         'comments': "It's a bit short",
         'date': datetime.date(2023, 3, 6)}
    ]

    fruit_reviews = [
        {'user': 'Kazzoe',
         'comments': "It's fruity",
         'date': datetime.date(2022, 2, 12)}
    ]

    cheese_reviews = [
        {'user': 'Kazzoe',
         'comments': "It's cheesy and Winter should definitely be cheddar; there should be more questions",
         'date': datetime.date(2020, 8, 7)}
    ]

    programming_outcomes = [
        'Object Oriented', 'Procedural', 'Functional', 'Imperative'
    ]

    fruit_outcomes = [
        'Orange', 'Apple', 'Strawberry', 'Pomegranate'
    ]

    cheese_outcomes = [
        'Gouda', 'Mozzarella', 'Parmesan', 'Emmental'
    ]

    pizza_answers = [
        'Cheese', 'Olives', 'Mushrooms', 'Pepperoni'
    ]

    colour_answers = [
        'Blue', 'Black', 'Red', 'Green'
    ]

    season_answers = [
        'Spring', 'Summer', 'Autumn', 'Winter'
    ]

    programming_questions = [
        {'description': 'Favourite pizza toppings?',
         'answers': pizza_answers}
    ]

    fruit_questions = [
        {'description': 'Favourite colour?',
         'answers': colour_answers}
    ]

    cheese_questions = [
        {'description': 'Favourite season?',
         'answers': season_answers}
    ]

    JasonQuizzes = [
        {'title': 'Which programming paradigm are you?',
         'description':'Take this simple quiz to discover which programming paradigm best represents you',
         'views': 7,
         'date': datetime.date(2023, 3, 6),
         'questions': programming_questions,
         'outcomes': programming_outcomes,
         'reviews' : programming_reviews},
        {'title': 'What fruit are you?',
         'description': 'Take this simple quiz to discover which fruit best represents you',
         'views': 2000,
         'date': datetime.date(2022, 1, 5),
         'questions': fruit_questions,
         'outcomes': fruit_outcomes,
         'reviews' : fruit_reviews}
    ]

    OtherQuizzes = [
        {'title': 'What type of cheese are you?',
         'description': 'Take this simple quiz to discover which cheese best represents you',
         'views': 2,
         'date': datetime.date(2020, 8, 7),
         'questions': cheese_questions,
         'outcomes': cheese_outcomes,
         'reviews' : cheese_reviews}
    ]

    Users = {
        'Jason': JasonQuizzes, 'JAS0N2003': OtherQuizzes
    }

    for user, quizlist in Users.items():
        up = add_user(user)
        for quiz in quizlist:
            q = add_quiz(up, quiz['title'], quiz['description'], quiz['views'], quiz['date'])
            for question in quiz['questions']:
                qu = add_question(q, question['description'])
                for answer in question['answers']:
                    add_answer(qu, answer)
            for outcome in quiz['outcomes']:
                add_outcome(q, outcome)
            for review in quiz['reviews']:
                add_review(q, review['user'], review['comments'], review['date'])


def add_user(username):
    u = User.objects.get_or_create(username=username)[0]
    up = UserProfile.objects.get_or_create(user=u)[0]
    u.save()
    up.save()
    return up

def add_quiz(user, title, description = "", views = 0, date = datetime.date(2000,1,1)):
    q = Quiz.objects.get_or_create(creator=user, title=title)[0]
    q.description = description
    q.views = views
    q.date = date
    q.save()
    return q

def add_question(quiz, description):
    qu = Question.objects.get_or_create(quiz=quiz, description=description)[0]
    qu.save()
    return qu

def add_answer(question, description):
    a = Answer.objects.get_or_create(question=question, description=description)[0]
    a.save()
    return a

def add_outcome(quiz, name):
    o = Outcome.objects.get_or_create(quiz=quiz, name=name)[0]
    o.save()
    return o

def add_review(quiz, user, comments, date):
    u = add_user(user)
    r = Review.objects.get_or_create(quiz=quiz, user=u, comments=comments, date = datetime.date(2000,1,1))[0]
    r.date = date
    r.save()
    return r

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

