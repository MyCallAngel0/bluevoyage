from django.shortcuts import render, redirect
from decorators.decorators import *


@redirect_if_authenticated(redirect_url="/test")
def registerTestPage(request):
    context = {}
    return render(request, 'register-test.html', context)

def logoutUser(request):
    return redirect('api/logout')


def homePage(request):
    context = {}
    return render(request, 'home.html', context)


@login_required(redirect_url='/login')
def randomPage(request):
    context = {}
    return render(request, 'random.html', context)

def testPage(request):
    context = {}
    return render(request, 'test.html', context)


@redirect_if_authenticated(redirect_url="/test")
def loginTestPage(request):
    context = {}
    return render(request, 'login-test.html', context)