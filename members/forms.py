from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from quiz.models import UserProfile
from django import forms

class ProfilePicForm(forms.ModelForm):
    picture = forms.ImageField(label="Profile Picture")

    class Meta:
        model = UserProfile
        fields = ('picture',)

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
