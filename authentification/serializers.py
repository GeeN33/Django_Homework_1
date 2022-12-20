from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentification.models import User
from ads.models import Location

def check_Users_birth_date(value: date):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 9 :
        raise ValidationError('users under 9 years old')

class Users_email:
    def __init__(self, email):
        self.email = email

    def __call__(self, value):

        m = value.split('@')
        if len(m) < 2:
            message = 'is not mail'
            raise serializers.ValidationError(message)

        if self.email == m[1]:

            message = f'can not use {self.email }'
            raise serializers.ValidationError(message)

class UsersSerializers(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "age", "location"]

class UsersCreateSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(many=True,
                                          queryset = Location.objects.all(),
                                          slug_field="name",
                                          required=False)
    birth_date = serializers.DateField(validators=[check_Users_birth_date])
    email = serializers.CharField(validators=[Users_email('rambler.ru'), UniqueValidator(queryset=User.objects.all()) ])
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "birth_date", "email", "location"]

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        for location in self._location:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_obj)
        user.save()
        return user

class UsersUpdateSerializers(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=True,
                                          queryset = Location.objects.all(),
                                          slug_field="name",
                                          required=False)
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "age", "location_id"]

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        for location in self._location:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_obj)
        user.save()
        return user

class UsersDestroySerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
