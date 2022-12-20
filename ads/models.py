from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date

def check_Categories(value):
    if len(value) < 5 or len(value) > 10:
        raise ValidationError('is not between 5 and 10')

class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True, validators=[check_Categories])
    def __str__(self):
        return self.name
    class Meta:
       verbose_name = 'Категория'
       verbose_name_plural = 'Категории'

class Ad(models.Model):
    from authentification.models import User

    name = models.SlugField(max_length=150, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь', null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=2000, blank=False)
    is_published = models.BooleanField(blank=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория', null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

class Selection(models.Model):
    name = models.CharField(max_length=50)
    owner = models.IntegerField()
    items = models.ManyToManyField(Ad)

    def __str__(self):
        return self.name
    class Meta:
       verbose_name = 'Подборка'
       verbose_name_plural = 'Подборки'