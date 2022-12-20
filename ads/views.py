import json
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.permissions import SelectionPermission, SelectionDeletePermission
from authentification.models import User
from ads.models import Ad, Categories, Location, Selection
from ads.serializers import LocationSerializers, AdSerializers, SelectionCreateSerializers, SelectionSerializers, \
    SelectionDetaiSerializers, SelectionUpdateSerializers, SelectionDestroySerializers, CategoriesSerializers, \
    AdCreateSerializers


def index(request):
    if request.method == "GET":
        return JsonResponse({"status": "ok"}, safe=False, status=200)
# Users

#Ad
class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        cat = request.GET.get('cat', None)
        if cat:
            self.queryset = self.queryset.filter(
                category__id=cat
            )

        text = request.GET.get('text', None)
        if text:
            self.queryset = self.queryset.filter(
                name__contains=text
            )

        location = request.GET.get('location', None)
        if location:
            self.queryset = self.queryset.filter(
                author_id__location__name=location
            )

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')

        if price_from and price_to:
            self.queryset = self.queryset.filter(
                price__range=(price_from, price_to)
            )

        return super().get(self, request, *args, **kwargs)

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "category_id"]
    def patch(self, request, *args, **kwargs):
        try:
            Ad.objects.get(pk=kwargs['pk'])
        except Ad.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the ad"}, status=404)
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.author_id = User.objects.get(id=ad_data["author"])
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = Categories.objects.get(id=ad_data["category"])

        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "name": self.object.name,
          "author_id": self.object.author_id,
          "author": User.objects.get(id=self.object.author_id_id).first_name,
          "price": self.object.price,
          "description": self.object.description,
          "is_published": self.object.is_published,
          "category_id": self.object.category_id,
          "image": self.object.image.url if self.object.image else ""

        }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
     model = Ad
     success_url = '/'
     def delete(self, request, *args, **kwargs):
         try:
             Ad.objects.get(pk=kwargs['pk'])
         except Ad.DoesNotExist:
             return JsonResponse({"error": "there is no such id in the ad"}, status=404)

         super().delete( request, *args, **kwargs)
         return JsonResponse({"status": "ok"}, status=200)

class AdDetailView(DetailView):
    model = Ad
    def get(self, request, *args, **kwargs):
        try:
          ad = Ad.objects.get(pk=kwargs['pk'])
        except Ad.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the ad"}, status=404)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category.name,
           }, safe=False, json_dumps_params={"ensure_ascii": True})

class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializers

@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "image"]
    def post(self, request, *args, **kwargs):
        try:
            Ad.objects.get(pk=kwargs['pk'])
        except Ad.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the ad"}, status=404)

        self.object = self.get_object()
        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "name": self.object.name,
          "author_id": self.object.author_id,
          "author": User.objects.get(id=self.object.author_id).first_name,
          "price": self.object.price,
          "description": self.object.description,
          "is_published": self.object.is_published,
          "category_id": self.object.category_id,
          "image": self.object.image.url if self.object.image else None

        }, safe=False, json_dumps_params={"ensure_ascii": True})

class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers

class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializers
    permission_classes = [IsAuthenticated, SelectionPermission]

class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializers

class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetaiSerializers


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializers
    permission_classes = [IsAuthenticated, SelectionPermission]

class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    permission_classes = [IsAuthenticated, SelectionDeletePermission]

