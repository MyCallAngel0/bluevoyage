from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .decorators import unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'bluevoyage/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'bluevoyage/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def homePage(request):
    context = {}
    return render(request, 'home.html', context)


@login_required(login_url='/login')
def randomPage(request):
    context = {}
    return render(request, 'random.html', context)