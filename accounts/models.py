from django.db import models
from django.contrib.auth.models import User


class UserHealth(models.Model):

    GOAL_CHOICES = (
        ('Weight Loss', 'Weight Loss'),
        ('Weight Gain', 'Weight Gain'),
        ('Maintain', 'Maintain'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    ACTIVITY_CHOICES = (
        ('Sedentary', 'Sedentary'),
        ('Light', 'Light'),
        ('Moderate', 'Moderate'),
        ('Active', 'Active'),
        ('Very Active', 'Very Active'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    mobile = models.CharField(max_length=10)

    age = models.IntegerField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    height = models.FloatField(
        help_text="Height in cm"
    )

    weight = models.FloatField(
        help_text="Weight in kg"
    )

    goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES,
        default='Maintain'
    )

    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        default='Moderate'
    )

    def __str__(self):
        return self.user.username