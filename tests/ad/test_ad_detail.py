import pytest
import json

@pytest.mark.django_db
def test_ad_detail(client, ad):
    expected_response = {
        "id": ad.pk,
        "name": "Добрый песик ищет хозяина",
        "author": ad.author.first_name,
        "price": 10,
        "description": "Толстовки с бесплатной доставкой в интернет-магазине Ламода, актуальные цены, в наличии большой ассортимент моделей.",
        "is_published": False,
        "category": ad.category.name
    }

    response = client.get(f"/ad/{ad.pk}/")

    data = json.loads(response.content)

    assert response.status_code == 200
    assert data  == expected_response