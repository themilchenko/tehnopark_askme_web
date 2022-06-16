from datetime import date
from django.contrib import messages
from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.management.commands.create_db import create_tag
from app.forms import SignInForm, UpdateProfile, CreateQuestion
from .models import Profile, Question, Tag, Answer, Like
from django.core.paginator import Paginator
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def hot_questions(request):
    hot_questions_db = Question.objects.filter(status='P')
    tags_db = Question.objects.filter(status='P')
    page_obj = Paginator(hot_questions_db, 10).get_page(
        request.GET.get('page'))

    if request.user.is_superuser:
        Profile.objects.update_or_create(profile=request.user)

    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        return render(request, "index.html", {'questions': hot_questions_db,
                                              'tags': tags_db,
                                              'page_obj': page_obj,
                                              'user': user})

    return render(request, "index.html", {'questions': hot_questions_db,
                                          'tags': tags_db,
                                          'page_obj': page_obj})


def new_questions(request):
    new_questions_db = Question.objects.order_by('-published_date')[:10]
    tags_db = Question.objects.all()
    page_obj = Paginator(new_questions_db, 10).get_page(
        request.GET.get('page'))

    if request.user.is_superuser:
        Profile.objects.update_or_create(profile=request.user)

    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        return render(request, "index.html", {'questions': new_questions_db,
                                              'tags': tags_db,
                                              'page_obj': page_obj,
                                              'user': user})

    return render(request, "index.html", {'questions': new_questions_db,
                                          'tags': tags_db,
                                          'page_obj': page_obj})


def tag_question(request, tag_id):
    questions = Question.objects.filter(tags=tag_id)
    tags_db = Question.objects.filter(status='P')
    page_obj = Paginator(questions, 10).get_page(
        request.GET.get('page'))

    return render(request, 'index.html', {'questions': questions, 'page_obj': page_obj, 'tags': tags_db})


def index(request):
    questions_db = Question.objects.all()
    tags_db = list()
    for item in Question.objects.all():
        if item.status == 'P':
            tags_db.append(Tag(name=item.get_tags))
    tags_db = Tag.objects.all()

    question_paginator = Paginator(questions_db, 10)
    question_page_obj = question_paginator.get_page(request.GET.get('page'))

    if request.user.is_superuser:
        Profile.objects.update_or_create(profile=request.user)

    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        return render(request, "index.html", {'questions': questions_db,
                                              'tags': tags_db,
                                              'question_page_obj': question_page_obj,
                                              'user': user})

    return render(request, "index.html", {'questions': questions_db,
                                          'tags': tags_db,
                                          'question_page_obj': question_page_obj})


def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, ('Incorrect username or password!'))
            return redirect('auth')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(profile=user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,  "You were registered successfully")
            return redirect('index')
    else:
        form = SignInForm()
    return render(request, 'sign-up.html', {'form': form})


def user_settings(request):
    message = None
    user = Profile.objects.get_avatar(username=request.user)
    if request.method == 'POST':
        form = UpdateProfile(request.POST,
                             request.FILES,
                             instance=request.user)
        if form.is_valid():
            form.save()
            message = 'Data has been saved'
    form = UpdateProfile(instance=request.user)
    return render(request, 'user-settings.html', {'form': form, 'msg': message, 'user': user})


def ask_question(request):
    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        form = CreateQuestion
        question = None
        if request.method == 'POST':
            form = CreateQuestion(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                tags = list()

                title = form.cleaned_data['title_text']
                text = form.cleaned_data['question_text']
                tags = form.cleaned_data['tag_field']

                tags = tags.split(' ')

                question = Question.objects.create(title_text=title,
                                                   question_text=text,
                                                   user=user,
                                                   published_date=date.today().strftime("%Y-%m-%d"),
                                                   status='N',
                                                   like=Like.objects.create(likes_count=0, dislikes_count=0))
                question.tags.set(create_tag(tags, title))
                messages.success(request, "Successfully created!")
                return redirect('view-question', question.id)
        return render(request, "ask-question.html", {'user': user, 'form': form, 'question': question})
    else:
        return redirect('auth')


def view_question(request, post_id, answer_id=None):
    question = get_object_or_404(Question, pk=post_id)
    tags_db = Tag.objects.all()
    answers_db = Answer.objects.filter(question=question)

    paginator = Paginator(answers_db, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    if request.method == 'POST':
        answer = request.POST.get('answer')
        Answer.objects.create(question=question,
                              user=Profile.objects.get_user(request.user),
                              answer_text=answer,
                              published_date=date.today().strftime("%Y-%m-%d"))

    if request.user.is_superuser:
        Profile.objects.update_or_create(profile=request.user)

    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        return render(request, "view-question.html", {'user': user,
                                                      'question': question,
                                                      'answer': answers_db,
                                                      'tags': tags_db,
                                                      'question_page_obj': page_obj})

    return render(request, "view-question.html", {'answer': answers_db,
                                                  'question': question,
                                                  'tags': tags_db,
                                                  'question_page_obj': page_obj})
