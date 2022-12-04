from django.db import models
from django.contrib.auth.models import AbstractUser



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

    def __str__(self):
        return self.name
    class Meta:
       verbose_name = 'Категория'
       verbose_name_plural = 'Категории'
class Ad(models.Model):
    from authentification.models import User

    name = models.SlugField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь', null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=2000)
    is_published = models.BooleanField()
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