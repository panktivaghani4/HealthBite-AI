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
    # ======================================
# Edit Profile Form
# ======================================

class UserHealthForm(forms.ModelForm):

    class Meta:
        model = UserHealth

        fields = [
            "profile_image",
            "mobile",
            "age",
            "gender",
            "height",
            "weight",
            "goal",
            "activity_level",
        ]

        widgets = {

             "profile_image": forms.FileInput(
                 attrs={
            "class": "form-control"
                }
            ),

            "mobile": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "age": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "height": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "goal": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "activity_level": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

        }