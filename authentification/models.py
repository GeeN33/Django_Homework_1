from django.db import models
from django.contrib.auth.models import AbstractUser
from ads.models import Location

class User(AbstractUser):


    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    location = models.ManyToManyField(Location)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["username"]

