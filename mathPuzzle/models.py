import datetime
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
import django.utils.timezone as timezone


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Задача")
    LOTO = 'LOTO'
    CARDS = 'CARDS'
    TEST = 'TEST'
    type_choices = (
        (LOTO, 'Лото'),
        (CARDS, 'Карточки'),
        (TEST, 'Тест')
    )
    type = models.CharField(verbose_name="Тип", max_length=10, choices=type_choices, default=TEST)
    date_published = models.DateTimeField(verbose_name="Дата публикации", default=datetime.datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class TaskResult(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name="Время ответа", default=timezone.now())
    result = models.IntegerField(verbose_name="Резултат", default=0)
    question_number = models.IntegerField(verbose_name="Номер последнего вопроса", default=0)


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name="Номер вопроса", default=1)
    title = models.CharField(max_length=200, verbose_name="Вопрос", default="question")
    date_published = models.DateTimeField(verbose_name="Дата публикации", default=timezone.now())
    image = models.ImageField(blank=True, upload_to='images/questions', verbose_name='ссылка картинки')
    SINGLE_ANSWER = 'single_answer'
    MULTIPLY_ANSWER = 'multiply_answer'
    OPEN_ANSWER = 'open_answer'
    type_choices = (
        (SINGLE_ANSWER, 'single_answer'),
        (MULTIPLY_ANSWER, 'multiply_answer'),
        (OPEN_ANSWER, 'open_answer')
    )
    type = models.CharField(max_length=200, verbose_name="Тип", choices=type_choices, default=SINGLE_ANSWER)
    right_answers = models.IntegerField(verbose_name="Кол-во правильных ответов", default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, verbose_name="Ответ", default="answer")
    is_right = models.BooleanField(verbose_name="Верный ответ?")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название школы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'


class SchoolClass(models.Model):
    name = models.CharField(max_length=3, verbose_name='Номер и буква класса')
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    GUEST = "GUEST"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    roles = (
        (GUEST, 'Гость'),
        (TEACHER, 'Учитель'),
        (STUDENT, 'Ученик'),
    )
    role = models.CharField(max_length=200, verbose_name="Роль", choices=roles, default=GUEST)
    # school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    school_class = models.ManyToManyField(SchoolClass)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.role
