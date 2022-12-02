from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MALE = "m"
    FEMALE = "f"
    SEX = [(MALE, "Male"), (FEMALE, "Female")]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)