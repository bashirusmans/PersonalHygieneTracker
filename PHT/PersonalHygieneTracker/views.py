from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
# Create your views here.

def loginPage(request):
    pagename = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if(user):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context = {'pagename':pagename}
    return render(request, 'PersonalHygieneTracker/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    if request.method == "POST":
        form = forms.MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")

    pagename = 'register'
    form = forms.MyUserCreationForm()
    context = {'pagename':pagename, 'form':form}
    return render(request, 'PersonalHygieneTracker/login_register.html', context)

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    if request.method == "POST":
        if user.username == request.POST.get('username'):
            pass
        else:
            try:
                named_user = models.User.objects.get(username=request.POST.get('username'))
                message = 'Username ' + named_user.username + ' is already taken'
                messages.error(request, message)
                return redirect('update-user')
            except:
                pass
        form = forms.UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, 'An error occured during updation')
    form = forms.UserForm(instance=user)
    context = {'form':form}
    return render(request, 'PersonalHygieneTracker/edit-user.html', context)

def home(request):

    context = {}
    return render(request, 'PersonalHygieneTracker/home.html', context)
