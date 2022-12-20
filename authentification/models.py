from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from ads.models import Location

class User(AbstractUser):

    role = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    location = models.ManyToManyField(Location)
    birth_date = models.DateField(null=True)
    email = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["username"]

