from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserHealth


class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)

    mobile = forms.CharField(max_length=10)

    age = forms.IntegerField()

    gender = forms.ChoiceField(
        choices=UserHealth.GENDER_CHOICES
    )

    height = forms.FloatField()

    weight = forms.FloatField()

    goal = forms.ChoiceField(
        choices=UserHealth.GOAL_CHOICES
    )

    activity_level = forms.ChoiceField(
        choices=UserHealth.ACTIVITY_CHOICES
    )

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'mobile',
            'age',
            'gender',
            'height',
            'weight',
            'goal',
            'activity_level',
            'password1',
            'password2'
        )