from urllib import request
from django.http import HttpResponse
from django.shortcuts import render

QUESTIONS = [
    {
        "title" : f'Title {i}',
        "text"  : f'This is text for question #{i}'
    } for i in range(10) 
]

def index(request):
    return render(request, 'index.html', {'questions' : QUESTIONS})

def auth(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'sign-up.html')

def authorized_user(request):
    return render(request, 'auth-user.html', {'questions' : QUESTIONS})

def ask_question(request):
    return render(request, 'ask-question.html')

def user_settings(request):
    return render(request, 'user-settings.html')    
