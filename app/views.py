
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import forms 
from . import models

# Create your views here.



def home(request):
    if request.user.is_authenticated:
        info = models.UserProfile.objects.get(user=request.user)
        context = {"info": info}
    else:
        context = {}
    return render(request, 'home.html', context)

def signup_view(request):
   
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            models.UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    context = { 'form': form }
    if request.user.is_authenticated:
        info = models.UserProfile.objects.get(user=request.user)
        context["info"] = info
    return render(request, 'Account/Signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home') 
    else:
        form = AuthenticationForm()
    context = { 'form': form }
    return render(request, 'Account/Login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def quiz_list(request):
    info = models.UserProfile.objects.get(user=request.user)
    quizs = models.Quizzes.objects.all()
    context = {"quizs": quizs, "info": info}
    return render(request, "Quizs/all_quizzes.html", context)