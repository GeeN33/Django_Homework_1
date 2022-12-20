import pytest
import json

@pytest.fixture()
@pytest.mark.django_db
def token(client, django_user_model):

    username = "admin"
    password = "admin"

    django_user_model.objects.create_user(first_name = "Матвей",
    last_name = "Иванов",
    username = username,
    password = password,
    email = "kjr88@mail.ru",
    birth_date = "2001-12-30",
    role = "member",
    age = 41)

    response = client.post(
        "/user/token/",
        {"username": username, "password": password},
        format='json'
    )
    data = json.loads(response.content)

    return data["access"]