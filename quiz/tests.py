import datetime
import importlib

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from quiz.models import UserProfile, Quiz, Question, Answer, Review, Outcome

class ViewTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('quiz.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('wad2_group_project.urls')

    def test_home_uses_template(self):
        self.response = self.client.get(reverse('quiz:home'))
        self.assertTemplateUsed(self.response, 'quiz/home.html')

    def test_view_exists(self):
        name_exists = 'home' in self.views_module_listing
        is_callable = callable(self.views_module.home)

        self.assertTrue(name_exists)
        self.assertTrue(is_callable)

class ModelTests(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username="username")

        userprofile = UserProfile.objects.get_or_create(user=user[0])

        quiz = Quiz.objects.get_or_create(title='Test', creator=userprofile[0], description="this is a test", views=55, date=datetime.date(2023,3,22))

        question = Question.objects.get_or_create(quiz=quiz[0], description="test question")

        Answer.objects.get_or_create(question=question[0], description="test answer", index=0)

        Outcome.objects.get_or_create(quiz=quiz[0], name="test outcome", index=0)

        Review.objects.get_or_create(quiz=quiz[0], user=userprofile[0], comments="test review", date=datetime.date(2023, 3, 23))

    def test_quiz_model(self):

        quiz = Quiz.objects.get(title='Test')
        self.assertEqual(quiz.views, 55)
        self.assertEqual(quiz.description, "this is a test")

        question = Question.objects.get(quiz=quiz)
        self.assertEqual(question.description, "test question")

        answer = Answer.objects.get(question=question)
        self.assertEqual(answer.description, "test answer")
        self.assertEqual(answer.index, 0)

        outcome = Outcome.objects.get(quiz=quiz)
        self.assertEqual(outcome.name, "test outcome")
        self.assertEqual(answer.index, outcome.index)

        review = Review.objects.get(quiz=quiz)
        self.assertEqual(review.comments, "test review")

    def test_str_method(self):
        quiz = Quiz.objects.get(title='Test')
        self.assertEqual(str(quiz), "Test")

        question = Question.objects.get(quiz=quiz)
        self.assertEqual(str(question), "test question")

        answer = Answer.objects.get(question=question)
        self.assertEqual(str(answer), "test answer")

        outcome = Outcome.objects.get(quiz=quiz)
        self.assertEqual(str(outcome), "test outcome")

        review = Review.objects.get(quiz=quiz)
        self.assertEqual(str(review), "test review")

        user = User.objects.get(username="username")
        userprofile = UserProfile.objects.get(user=user)
        self.assertEqual(str(userprofile), "username")
