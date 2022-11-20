from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name
class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    age = models.IntegerField()
    location = models.ManyToManyField(Location)
    def __str__(self):
        return self.first_name
    class Meta:
       verbose_name = 'Пользователь'
       verbose_name_plural = 'Пользователи'
       ordering = ["username"]
class Categories(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    class Meta:
       verbose_name = 'Категория'
       verbose_name_plural = 'Категории'
class Ad(models.Model):
    name = models.SlugField(max_length=150)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name = 'Пользователь', null=True)
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

