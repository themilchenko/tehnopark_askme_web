import random
import string
import time
import datetime
from datetime import date, datetime
from turtle import color, title
from django.core.management.base import BaseCommand, CommandError
from tomlkit import datetime
from app.models import Answer, Question, Tag, Profile, Like
from django.contrib.auth.models import User


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)


def generate_color():
    return ['r', 'g', 'y'][random.randint(0, 2)]


def random_string(start, end):
    number = random.randint(start, end)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=number))


def create_user_db(name):
    user = User.objects.create_user(username=name, email='{0}@{1}.ru'.format(
        random_string(10, 25), random_string(2, 5)), password=random_string(5, 15))
    return Profile.objects.create(profile=user)


def create_tag_db(num, question_title):
    result = list()
    for i in range(num):
        result.append(Tag.objects.create(
            color=generate_color(), name=random_string(3, 5), question_title=question_title))
    return result


def create_like(likes_num, dislikes_num):
    return Like.objects.create(likes_count=likes_num, dislikes_count=dislikes_num)


def create_question_answers_db(num):
    for i in range(num):
        question = Question.objects.create(title_text=random_string(3, 10), 
                                           question_text=random_string(100, 300), 
                                           user=create_user_db(random_string(3, 10)), 
                                           answers_count=random.randint(3, 33), 
                                           like=create_like(random.randint(0, 100), random.randint(0, 50)), 
                                           published_date=random_date("2022-1-1", date.today().strftime("%Y-%m-%d"), random.random()))
        question.tags.set(create_tag_db(random.randint(3, 5), question.title_text))

        for j in range(random.randint(5, 25)):
            Answer.objects.create(question=question, user=question.user, answer_text=random_string(
                20, 30), published_date=date.today().strftime("%Y-%m-%d"))

        

        # counting num of answers
        for item in Question.objects.all():
            item.answers_count = Answer.objects.filter(question=item).count()
            item.save()

        # determining of popular state
        for item in Question.objects.all():
            if item.get_likes() + item.get_dislikes() > 100:
                item.status = 'P'
                item.save()

        # determining of new state
        for item in Question.objects.all():
            if abs(item.published_date.month == date.today().month ):
                item.status = 'N'
                item.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('question_count', nargs='+', type=int)

    def handle(self, *args, **options):
        create_question_answers_db(options['question_count'][0])
