import factory

from ads.models import Ad, Categories, Location
from authentification.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "Матвей"
    last_name = "Иванов"
    username = factory.Faker("name")
    password = "password"
    email = "kjr88@mail.ru"
    birth_date = "2001-12-30"
    role = "member"
    age = 41
    # location = factory.SubFactory(LocationFactory)

class CategoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories

    name= "Одежда"
    slug= factory.Faker("name")

class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "Добрый песик ищет хозяина"
    author = factory.SubFactory(UserFactory)
    price = 10
    description = "Толстовки с бесплатной доставкой в интернет-магазине Ламода, актуальные цены, в наличии большой ассортимент моделей."
    is_published = False
    category = factory.SubFactory(CategoriesFactory)