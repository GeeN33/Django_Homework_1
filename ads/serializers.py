from django.core.exceptions import ValidationError
from rest_framework import serializers

from ads.models import Location, Categories, Ad, Selection
from authentification.models import User

def check_Ad_name(value):
    if len(value) < 10:
        raise ValidationError('name must contain at least 10 characters')

def check_Ad_is_published(value: bool):
    if value :
        raise ValidationError('cant be True')

def check_Ad_price(value):
    if value <= 0:
        raise ValidationError('cannot be zero or less')

class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class AdSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(),   slug_field="first_name",  required=False)
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field="name", required=False)
    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "description", "is_published",  "category"]

class AdCreateSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(),   slug_field="first_name",  required=False)
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field="name", required=False)
    name = serializers.CharField(validators=[check_Ad_name])
    is_published = serializers.BooleanField(validators=[check_Ad_is_published])
    price = serializers.IntegerField(validators=[check_Ad_price])
    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "description", "is_published", "category"]


    def is_valid(self, *, raise_exception=False):
        self._author = self.initial_data.pop("author_id")
        self._category = self.initial_data.pop("category_id")
        return super().is_valid(raise_exception=raise_exception)
    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        try:
            ad.author = User.objects.get(id=self._author)
        except User.DoesNotExist:
            raise ValidationError("Users not")

        try:
              ad.category = Categories.objects.get(id=self._category)
        except Categories.DoesNotExist:
            raise ValidationError("Categories not")

        ad.save()
        return ad

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
    author = serializers.SlugRelatedField(queryset=User.objects.all(),   slug_field="id",  required=False)
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