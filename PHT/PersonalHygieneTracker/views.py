from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from datetime import datetime
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
    count = models.Category.objects.filter(user=request.user).count()
    if count >= 9:
        add = False
    else:
        add = True
    categories = models.Category.objects.filter(user__isnull=True)
    user_categories = models.Category.objects.filter(user=request.user)
    context = {'categories':categories, 'user_categories': user_categories, 'add':add}
    return render(request, 'PersonalHygieneTracker/home.html', context)

@login_required(login_url="login")
def category(request, pk):
    category = models.Category.objects.get(id=int(pk))
    routines = category.routine_set.all().order_by('-time')
    context = {'routines':routines, 'category':category}
    return render(request, 'PersonalHygieneTracker/category.html', context)

@login_required(login_url="login")
def addCategory(request):
    count = models.Category.objects.filter(user=request.user).count()
    if count>=9:
        messages.error(request, 'You cannot have more than 9 custom categories')
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name')
        new_category, created = models.Category.objects.get_or_create(name=name, user=request.user)
        if not created:
            messages.error(request, 'A category with that name already exists')
        else:
            return redirect('home')
    context = {'count':count}
    return render(request, 'PersonalHygieneTracker/add_category.html', context)

@login_required(login_url="login")
def routine(request, pk):
    routine = models.Routine.objects.get(id=int(pk))
    context = {'routine':routine}
    return render(request, 'PersonalHygieneTracker/routine.html', context)

@login_required(login_url="login")
def addRoutine(request, pk):
    category = models.Category.objects.get(id=int(pk))
    user = request.user
    if category.user:
        if user != category.user:
            return redirect('home')
    if request.method == 'POST':
        monday = 'monday' in request.POST
        tuesday = 'tuesday' in request.POST
        wednesday = 'wednesday' in request.POST
        thursday = 'thursday' in request.POST
        friday = 'friday' in request.POST
        saturday = 'saturday' in request.POST
        sunday = 'sunday' in request.POST
        task = request.POST.get('task')
        description = request.POST.get('description')
        time = request.POST.get('time')

        # Convert the string to a time object
        time_object = datetime.strptime(time, "%I:%M %p").time()

        new_routine, created = models.Routine.objects.get_or_create(user=user, category=category, task=task, description=description, time=time_object, monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)
        if not created:
            messages.error(request, 'An error occured during creation. Please fill all fields with valid data')
        else:
            pk = new_routine.category.pk
            return redirect('category', pk=pk)
    context = {'category':category}
    return render(request, 'PersonalHygieneTracker/add_routine.html', context)

@login_required(login_url="login")
def profile(request, pk):
    user = models.User.objects.get(id=int(pk))
    context = {'user':user}
    return render(request, 'PersonalHygieneTracker/profile.html', context)

@login_required(login_url="login")
def deleteCategory(request, pk):
    category = models.Category.objects.get(id=int(pk))
    if request.user != category.user:
        return HttpResponse("You are not allowed to delete this category")
    if request.method == 'POST':
        category.delete()
        return redirect('home')
    context = {'obj': category}
    return render(request, 'PersonalHygieneTracker/delete.html', context)

@login_required(login_url="login")
def deleteRoutine(request, pk):
    routine = models.Routine.objects.get(id=int(pk))
    if request.user != routine.user:
        return HttpResponse("You are not allowed to delete this routine")
    if request.method == 'POST':
        pk = routine.category.id
        routine.delete()
        return redirect('category', pk=pk)
    context = {'obj': routine}
    return render(request, 'PersonalHygieneTracker/delete.html', context)


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
            print(form)
            form.save()
            return redirect('profile', pk=user.id)
        else:
            messages.error(request, 'An error occured during updation')
    form = forms.UserForm(instance=user)
    context = {'form': form}
    return render(request, 'PersonalHygieneTracker/edit-user.html', context)
