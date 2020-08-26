from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from mathPuzzle.models import School, SchoolClass


def validate_school_choice(choice):
    if choice == '-1':
        raise ValidationError(
            'Необходимо выбрать школу',
            params={'choice': choice}
        )


def validate_school_class_choice(choice):
    if choice == '-1':
        raise ValidationError(
            'Необходимо выбрать класс',
            params={'choice': choice}
        )


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class VerificationForm(forms.Form):
    schools = list(School.objects.values())
    school_classes = list(SchoolClass.objects.values())
    school_choices = [(-1, 'Выбрать Школу')]
    school_class_choices = [(-1, 'Выбрать класс')]
    for school in schools:
        school_choices.append((school['id'], school['name']))
    for school_class in school_classes:
        school_class_choices.append((school_class['id'], school_class['name']))

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    school = forms.ChoiceField(choices=school_choices,
                               widget=forms.Select(attrs={'id': 'school_select'}),
                               validators=[validate_school_choice])

    school_class = forms.ChoiceField(choices=school_class_choices,
                                     widget=forms.Select(attrs={'disabled': 'false', 'id': 'school_class_select'}),
                                     validators=[validate_school_class_choice])
