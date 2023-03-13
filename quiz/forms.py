from django import forms
from quiz.models import Quiz, Outcome, Question, Answer, UserProfile

class QuizForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text = "Please enter a quiz title.", required=True)
    description = forms.CharField(max_length = 255, help_text = "Please enter an informative description for your quiz.",required=True)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Quiz
        fields = ('title', 'description',)

class OutcomeForm(forms.ModelForm):
    name = forms.CharField(max_length = 255, help_text = "Please enter an outcome for your quiz.", required=True)
    ##image = forms.ImageField(help_text = "Please upload an image of your outcome.")

    class Meta:
        model = Outcome
        exclude = ('quiz', 'index')

class QuestionForm(forms.ModelForm):
    description = forms.CharField(max_length = 255, help_text = "Please enter a question description:", required=True)

    class Meta:
        model = Question
        exclude = ('quiz',)

class AnswerForm(forms.ModelForm):
    description = forms.CharField(max_length = 255, help_text = "Please enter an answer associated with outcome ", required=True)

    class Meta:
        model = Answer
        exclude = ('question', 'index')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
