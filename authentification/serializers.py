from rest_framework import serializers

from authentification.models import User
from ads.models import Location

# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#
#         user.set_password(validated_data["password"])
#         user.save()
#
#         return user

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
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "age", "location"]

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
