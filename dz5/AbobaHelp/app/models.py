from AbobaHelp import settings

from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def with_tag(self, tag):
        return self.filter(tags__id=tag)
    def best(self):
        return self.annotate(like__sum=Coalesce(Sum('questionlike__like'), 0)).order_by('-like__sum')
    
    def newest(self):        
        return self.get_queryset().order_by('-creation_date')
    

class AnswerManager(models.Manager):
    def best(self):
        return self.annotate(like__sum=Coalesce(Sum('answerlike__like'), 0)).order_by('-correct', '-like__sum')


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64)
    avatar = models.ImageField(upload_to='img/avatars', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user_id} {self.nickname}"


class Tag(models.Model):
    name = models.CharField(max_length=32)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"
    

class Question(models.Model):
    author = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    
    objects = QuestionManager()

    @property
    def rating(self):
        return QuestionLike.objects.filter(question=self).aggregate(like__sum=Coalesce(Sum('like'), 0)).get('like__sum')
    
    @property
    def answer_count(self):
        return Answer.objects.filter(question=self).count()
    
    @property
    def liked_by(self):
        return self.questionlike_set.values_list('author', flat=True)

    def __str__(self) -> str:
        return f"{self.author_id} {self.title[0:16]} {self.text[0:16]}"


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    
    def __str__(self) -> str:
        return f"{self.question_id} {self.author_id} {self.like}"

    class Meta:
        unique_together = ('question', 'author')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=False)

    objects = AnswerManager()

    @property
    def rating(self):
        return AnswerLike.objects.filter(answer=self).aggregate(like__sum=Coalesce(Sum('like'), 0)).get('like__sum')
    
    @property
    def liked_by(self):
        return self.answerlike_set.values_list('author', flat=True)

    def __str__(self) -> str:
        return f"{self.author_id} {self.text[0:16]} {self.correct}"


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    def __str__(self) -> str:
        return f"{self.answer_id} {self.author_id} {self.like}"

    class Meta:
        unique_together = ('answer', 'author')