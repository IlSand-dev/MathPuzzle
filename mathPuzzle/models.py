import datetime
from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name="Question")
    date_published = models.DateTimeField(verbose_name="Published_Date", default=datetime.datetime.now())


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    is_right = models.BooleanField()
