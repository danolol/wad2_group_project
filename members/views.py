from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterUserForm, ProfilePicForm
from quiz.models import UserProfile

# Create your views here.
def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in, Try Again"))
            print("Error")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})
    


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('home')


def register_user(request):

    if request.method == "POST":
        form = RegisterUserForm(request.POST, request.FILES or None)
        pfp_form = ProfilePicForm(request.POST, request.FILES or None)

        if form.is_valid() and pfp_form.is_valid():
            user = form.save()
            pic, created = UserProfile.objects.get_or_create(user=user)
            pic.picture = pfp_form.cleaned_data['picture']
            pic.save()


            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registered Successfully"))
            return redirect('home')
    else:
        form = RegisterUserForm()
        pfp_form = ProfilePicForm()

    return render(request, 'authenticate/registration.html', {'form':form, 'pfp_form':pfp_form})
    

