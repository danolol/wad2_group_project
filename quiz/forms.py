from django import forms
from quiz.models import Quiz, Outcome, Question, Answer, UserProfile, Review

class QuizForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text = "Please enter a quiz title.", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length = 255, help_text = "Please enter an informative description for your quiz.",required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Quiz
        fields = ('title', 'description',)

class OutcomeForm(forms.ModelForm):
    name = forms.CharField(max_length = 255, help_text = "Please enter an outcome for your quiz.", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(help_text = "Please upload an image of your outcome.", required=True, widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Outcome
        exclude = ('quiz', 'index')

class QuestionForm(forms.ModelForm):
    description = forms.CharField(max_length = 255, help_text = "Please enter a question description:", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Question
        exclude = ('quiz',)

class AnswerForm(forms.ModelForm):
    description = forms.CharField(max_length = 255, help_text = "Please enter an answer associated with outcome ", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Answer
        exclude = ('question', 'index')

# changes here
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comments', )
