from  django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.http import HttpResponse
from administration.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from allauth.account.views import LoginView, SignupView 

def Inactive(request):
    return HttpResponse("<h1>You are inactive.<br>Please contact administration.</h1>")

def SignupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        user = authenticate(request,email=email, password=password)
        print(password)
        if user:
            login(request, user)    
            return redirect('home')
        else:
            Result="Email password doesnt matched"
            return render(request, 'account/login.html', {'results': Result})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})




def Logout(request):
    logout(request)
    return redirect('login')

#     # if request.method == 'POST':
#     #     username=request.POST.

#     #     usr= User(password="qwertyuiop345",  username="bhuban31", email="bhuban@gmail.com", first_name="bhuban", last_name="ghimire")
#     #     usr.save()
#     # return render(request, 'account/signup.html')
