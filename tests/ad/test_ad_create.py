import pytest
import json

from ads.models import Categories
from authentification.models import User


@pytest.mark.django_db
def test_ad_create(client, token):
    expected_response = {
        "id": 1,
        "name": "Добрый песик ищет хозяина",
        "author": "Матвей",
        "price": 10,
        "description": "Толстовки с бесплатной доставкой в интернет-магазине Ламода, актуальные цены, в наличии большой ассортимент моделей.",
        "is_published": False,
        "category": "test"
    }
    data = {
            "name": "Добрый песик ищет хозяина",
            "author_id": 1,
            "price": 10,
            "description": "Толстовки с бесплатной доставкой в интернет-магазине Ламода, актуальные цены, в наличии большой ассортимент моделей.",
            "is_published": False,
            "category_id": 1 }


    # User.objects.create(first_name = "Матвей",
    # last_name = "Иванов",
    # username = "name",
    # password = "password",
    # email = "kjr88@mail.ru",
    # birth_date = "2001-12-30",
    # role = "member",
    # age = 41)
    Categories.objects.create(name="test",slug="test")

    response = client.post("/ad/create/", data=data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)

    data2 = json.loads(response.content)

    assert response.status_code == 201
    assert data2  == expected_response