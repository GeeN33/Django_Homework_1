from django.db import models

class Ads(models.Model):
    name = models.SlugField(max_length=150)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField()


class Categories(models.Model):
    name = models.SlugField(max_length=150)
