from rest_framework import serializers

from ads.models import Location, Users, Categories, Ad, Selection


class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class UsersSerializers(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    class Meta:
        model = Users
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "age", "location"]

class UsersCreateSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(many=True,
                                          queryset = Location.objects.all(),
                                          slug_field="name",
                                          required=False)
    class Meta:
        model = Users
        fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "age", "location"]

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = Users.objects.create(**validated_data)
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
        model = Users
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
        model = Users
        fields = ["id"]

class AdSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Users.objects.all(),   slug_field="first_name",  required=False)
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field="name", required=False)
    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "category"]

class SelectionCreateSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = serializers.SlugRelatedField(many=True,
                                          queryset = Ad.objects.all(),
                                          slug_field="id",
                                          required=False)
    owner = serializers.IntegerField()
    class Meta:
        model = Selection
        fields = ["id", "name", "owner", "items"]

    def is_valid(self, *, raise_exception=False):
        self._items = self.initial_data.pop("items")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        selection = Selection.objects.create(**validated_data)
        for items in self._items:
            ad_obj, _ = Ad.objects.get_or_create(id=items)
            selection.items.add(ad_obj)
        selection.save()
        return selection

class SelectionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ["id", "name"]

class SelectionAdSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Users.objects.all(),   slug_field="id",  required=False)
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field="id", required=False)
    class Meta:
        model = Ad
        fields = ["id", "name", "price","description","is_published","image", "author","category"]

class SelectionDetaiSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = SelectionAdSerializers(many=True, read_only=True)
    class Meta:
        model = Selection
        fields = ["id", "items", "name", "owner"]

class SelectionUpdateSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = serializers.SlugRelatedField(many=True,
                                         queryset=Ad.objects.all(),
                                         slug_field="id",
                                         required=False)
    owner = serializers.IntegerField()

    class Meta:
        model = Selection
        fields = ["id", "name", "owner", "items"]


    def is_valid(self, *, raise_exception=False):
        self._items = self.initial_data.pop("items")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        selection = super().save()
        for item in self._items:
            ad_obj, _ = Ad.objects.get_or_create(id=item)
            selection.items.add(ad_obj)
        selection.save()
        return selection

class SelectionDestroySerializers(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]