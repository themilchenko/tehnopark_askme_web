from datetime import date
from django.contrib import messages
from urllib import request
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from app.management.commands.create_db import create_tag
from app.forms import SignInForm, UpdateProfile, CreateQuestion, UpdateUser
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
    # form = None
    profile = Profile.objects.get_user(request.user)
    profile_form = UpdateProfile(instance=profile)
    user_form = UpdateUser(instance=request.user)

    if request.method == 'POST':
        user_form = UpdateUser(request.POST, instance=request.user)
        profile_form = UpdateProfile(
            request.POST, request.FILES, instance=profile)
        if user_form.is_valid():
            user_form.save()
        if profile_form.is_valid():
            profile_form.save()

    return render(request, 'user-settings.html', {'profile_form': profile_form,
                                                  'user_form': user_form,
                                                  'user': Profile.objects.get_avatar(username=request.user)})


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
                                                   status='N')
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
        question.answers_count += 1
        question.save()

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


def vote(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            type = request.POST['type']
            object_id = request.POST['question_id']
            object_vote = int(request.POST['vote'])
            obj = None
            if type == 'question':
                obj = Question.objects.get(id=object_id)
            else:
                obj = Answer.objects.get(id=object_id)

            vote = None
            if type == 'question':
                try:
                    vote = Like.objects.get(question=obj, user=request.user)
                except Like.DoesNotExist:
                    vote = Like(question=obj, user=request.user)
                    vote.save()
            else:
                try:
                    vote = Like.objects.get(answer=obj, user=request.user)
                except Like.DoesNotExist:
                    vote = Like(answer=obj, user=request.user)
                    vote.save()

            if object_vote == 0:
                if vote is not None:
                    if vote.is_like == True:
                        vote.is_like = False
                        obj.likes_count -= 1
                    elif vote.is_dislike == True:
                        vote.is_like = True
                        vote.is_dislike = False
                        obj.dislikes_count -= 1
                        obj.likes_count += 1
                    else:
                        vote.is_like = True
                        obj.likes_count += 1
                    vote.save()
                else:
                    if type == 'question':
                        Like.objects.create(
                            is_like=True, user=request.user, question=obj)
                    else:
                        Like.objects.create(
                            is_like=True, user=request.user, answer=obj)
                    obj.likes_count += 1
            else:
                if vote is not None:
                    if vote.is_dislike == True:
                        vote.is_dislike = False
                        obj.dislikes_count -= 1
                    elif vote.is_like == True:
                        vote.is_dislike = True
                        vote.is_like = False
                        obj.dislikes_count += 1
                        obj.likes_count -= 1
                    else:
                        vote.is_dislike = True
                        obj.dislikes_count += 1
                    vote.save()
                else:
                    if type == 'question':
                        Like.objects.create(
                            is_dislike=True, is_like=False, user=request.user, question=obj)
                    else:
                        Like.objects.create(
                            is_dislike=True, is_like=False, user=request.user, answer=obj)
                    obj.dislikes_count += 1

            obj.save()
            return JsonResponse({'current_likes': obj.likes_count,
                                 'current_dislikes': obj.dislikes_count})
    else:
        return redirect('auth')
