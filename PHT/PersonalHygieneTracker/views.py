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
    main = True

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if(user):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password does not exist')


    context = {'pagename':pagename, 'main':main}
    return render(request, 'PersonalHygieneTracker/login_register.html', context)

@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect('index')

def registerUser(request):
    main = True
    if request.method == "POST":
        form = forms.MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "An error occured during registration")

    pagename = 'register'
    form = forms.MyUserCreationForm()
    context = {'pagename':pagename, 'form':form, 'main':main}
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

def index(request):
    main = True
    context = {'main':main}
    return render(request, 'PersonalHygieneTracker/index.html', context)

@login_required(login_url="login")
def home(request):
    categories = models.Category.objects.filter(user__isnull=True)
    user_categories = models.Category.objects.filter(user=request.user)
    context = {'categories':categories, 'user_categories': user_categories}
    return render(request, 'PersonalHygieneTracker/home.html', context)

@login_required(login_url="login")
def category(request, pk):
    category = models.Category.objects.get(id=int(pk))
    routines = category.routine_set.all().order_by('-time')
    context = {'routines':routines}
    return render(request, 'PersonalHygieneTracker/category.html', context)

def profile(request, pk):
    user = models.User.objects.get(id=int(pk))
    context = {'user':user}
    return render(request, 'PersonalHygieneTracker/profile.html', context)