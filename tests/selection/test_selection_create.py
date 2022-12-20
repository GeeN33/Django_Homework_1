import pytest
import json

from ads.models import Categories, Ad
from authentification.models import User


@pytest.mark.django_db
def test_selection_create(client, token):
    expected_response = {
    "id": 1,
    "name": "Подборка Васи",
    "owner": 1,
    "items": [1]}

    data = {
	"name": "Подборка Васи",
	"owner": 1,
	"items": [1]}


    Categories.objects.create(name="test",slug="test")

    Ad.objects.create(
    name="Добрый песик ищет хозяина",
    author = User.objects.get(id=1),
    price = 10,
    description = "Толстовки с бесплатной доставкой в интернет-магазине Ламода, актуальные цены, в наличии большой ассортимент моделей.",
    is_published = False,
    category = Categories.objects.get(id=1),
    )



    response = client.post("/selection/create/", data=data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)

    data2 = json.loads(response.content)

    assert response.status_code == 201
    assert data2  == expected_response