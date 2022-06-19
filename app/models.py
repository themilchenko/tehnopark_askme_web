from argparse import _MutuallyExclusiveGroup
import profile
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def get_tag(self, tag):
        return Question.objects.filter(tag_name=tag)


class LikeManager(models.Manager):
    def get_likes(self, question):
        return Like.objects.filter(question=question, is_like=True).count()

    def get_dislikes(self, question):
        return Like.objects.filter(question=question, is_dislike=True).count()


class ProfileManager(models.Manager):
    def get_avatar(self, username):
        return Profile.objects.get(profile=username).avatar

    def get_user(self, username):
        return Profile.objects.get(profile=username)


class Profile(models.Model):
    profile = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name='User')
    avatar = models.ImageField(default='profile-default.png', upload_to='', null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.profile.username


class Tag(models.Model):
    color = models.CharField(max_length=1, null=True, blank=True, default='g')
    name = models.CharField(max_length=32)
    question_title = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    STATUS = [
        ('P', 'Popular question'),
        ('N', 'New question'),
        ('D', 'Not determinded')
    ]

    title_text = models.CharField(max_length=64, null=False, blank=True)
    question_text = models.TextField(unique=True)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='user')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    tag_field = models.CharField(max_length=64, blank=True, null=True)
    answers_count = models.IntegerField(null=True, default=0)

    status = models.CharField(max_length=1, choices=STATUS, default='D')

    published_date = models.DateField(null=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    objects = QuestionManager()

    def get_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.title_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer_text = models.TextField(default='')
    published_date = models.DateField()
    is_correct = models.BooleanField(default=False)

    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    def get_question_title(self):
        return self.question.title_text

    def get_question_text(self):
        return self.question.question_text


class Like(models.Model):
    is_like = models.BooleanField(default=False, null=True)
    is_dislike = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer', null=True)

    objects = LikeManager()
