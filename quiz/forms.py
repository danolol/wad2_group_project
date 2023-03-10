from django import forms
<<<<<<< HEAD
from quiz.models import Quiz, Outcome, Question, Answer

class QuizForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text = "Please enter a quiz title.")
    description = forms.CharField(max_length = 255, help_text = "Please enter an informative description for your quiz.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    date = forms.DateField(widget=forms.HiddenInput())
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Quiz
        fields = ('name', 'description')

class OutcomeForm(forms.ModelForm):
    name = forms.CharField(max_length = 255, help_text = "Please enter an outcome for your quiz.")
    image = forms.ImageField(upload_to='outcome_images', help_text = "Please upload an image of your outcome.")
    index = forms.IntegerField(widget = forms.HiddenInput(), min_value=0, max_value=3)

    class Meta:
        model = Outcome
        exclude = ('quiz')

class QuestionForm(forms.ModelForm):
    description = forms.CharField(max_length = 255, help_text = "Please enter a question description.")

    class Meta:
        model = Question
        exclude = ('quiz')

class AnswerForm(forms.ModelForm):
    description = forms.CharField(max_length = 255, help_text = "Please enter an answer associated with {x} outcome")
    index = forms.IntegerField(widget = forms.HiddenInput(), min_value=0, max_value=3)

    class Meta:
        model = Answer
        exclude = ('question')



=======
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
>>>>>>> main
