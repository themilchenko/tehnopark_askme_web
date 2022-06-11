from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question, Tag, Answer, Like
from django.core.paginator import Paginator
from django.views.generic import DeleteView


def hot_questions(request):
    hot_questions_db = Question.objects.filter(status='P')
    tags_db = Question.objects.filter(status='P')
    page_obj = Paginator(hot_questions_db, 10).get_page(
        request.GET.get('page'))

    return render(request, 'index.html', {'questions': hot_questions_db, 'page_obj': page_obj, 'tags': tags_db})


def new_questions(request):
    new_questions_db = Question.objects.filter(status='N')
    tags_db = Question.objects.filter(status='P')
    page_obj = Paginator(new_questions_db, 10).get_page(
        request.GET.get('page'))

    return render(request, 'index.html', {'questions': new_questions_db, 'page_obj': page_obj, 'tags': tags_db})


def tag_question(request, tag_id):
    questions = Question.objects.filter(tags=tag_id)
    tags_db = Question.objects.filter(status='P')
    page_obj = Paginator(questions, 10).get_page(
        request.GET.get('page'))

    return render(request, 'index.html', {'questions': questions, 'page_obj': page_obj, 'tags': tags_db})



def index(request):
    questions_db = Question.objects.all()
    tags_db = []
    for item in Question.objects.all():
        if item.status == 'P':
            tags_db.append(Tag(name=item.get_tags))
    tags_db = Tag.objects.all()

    paginator = Paginator(questions_db, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'index.html',
                           {
                               'questions': questions_db,
                               'tags': tags_db,
                               'page_obj': page_obj
                           })


def auth(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'sign-up.html')


def authorized_user(request):
    questions_db = Question.objects.all()
    tags_db = Tag.objects.all()
    return render(request, 'auth-user.html', {'questions': questions_db, 'tags': tags_db})


def ask_question(request):
    return render(request, 'ask-question.html')


def user_settings(request):
    return render(request, 'user-settings.html')


def view_question(request, post_id):
    question = get_object_or_404(Question, pk=post_id)
    tags_db = Tag.objects.all()
    answers_db = Answer.objects.filter(question=question)

    paginator = Paginator(answers_db, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'view-question.html', {'answer': answers_db,
                                                  'tags': tags_db,
                                                  'page_obj': page_obj
                                                  })
