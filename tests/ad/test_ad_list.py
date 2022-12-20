import pytest
import json

from ads.serializers import AdSerializers
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ads = AdFactory.create_batch(5)
    dict_ads=[]
    for ad_ in ads:
        dict_ads.append({
            "id": ad_.id,
            "name": ad_.name,
            "author": ad_.author.first_name,
            "price": ad_.price,
            "description": ad_.description,
            "is_published": ad_.is_published,
            "category": ad_.category.name
        }
        )


    expected_response = {
        "count": 5,
        "next": None,
        "previous": None,
         "results": dict_ads
    }

    response = client.get(f"/ad/")

    data = json.loads(response.content)

    assert response.status_code == 200
    assert data  == expected_response