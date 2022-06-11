from argparse import _MutuallyExclusiveGroup
from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def get_tag(self, tag):
        return Question.objects.filter(tag__name=tag)


class ProfileManager(models.Manager):
    def get_user(self, user):
        return Profile.objects.get(username=user)


class Profile(models.Model):
    profile = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name='User')
    avatar = models.ImageField(null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.profile.username


class Like(models.Model):
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.likes_count)


class Tag(models.Model):
    color = models.CharField(max_length=1, null=True, blank=True, default='g')
    name = models.CharField(max_length=32, unique=True)
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
    question_text = models.TextField()
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='user')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    answers_count = models.IntegerField(null=True)

    status = models.CharField(max_length=1, choices=STATUS, default='D')

    published_date = models.DateField(null=True)
    like = models.ForeignKey(
        Like, on_delete=models.CASCADE, related_name='like', blank=True, null=True)

    objects = QuestionManager()

    def get_likes(self):
        return self.like.likes_count

    def get_dislikes(self):
        return self.like.dislikes_count

    def get_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.title_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer_text = models.TextField(default='')
    published_date = models.DateField()

    def get_question_title(self):
        return self.question.title_text

    def get_question_text(self):
        return self.question.question_text

