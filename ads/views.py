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

from ads.models import Ad, Categories, Users, Location, Selection
from ads.serializers import LocationSerializers, UsersSerializers, UsersCreateSerializers, CategoriesSerializers, \
    UsersUpdateSerializers, UsersDestroySerializers, AdSerializers, SelectionCreateSerializers, SelectionSerializers, \
    SelectionDetaiSerializers, SelectionUpdateSerializers, SelectionDestroySerializers


def index(request):
    if request.method == "GET":
        return JsonResponse({"status": "ok"}, safe=False, status=200)
# Users
class UsersListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializers

class UsersDetailView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializers

class UsersCreateView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersCreateSerializers

class UsersUpdateView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersUpdateSerializers

class UsersDeleteView(DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersDestroySerializers

class UsersZView(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            # total_ads = Ad.objects.filter(author_id=user, is_published=True).count()
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(user.location.all().values_list("name", flat=True)),
                "total_ads": user.total_ads
                })
        response = {
            "items": users,
            "total":paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": True})
        # rez = Users.objects.filter(age=24).count()
        #
        # return HttpResponse(rez)

#Ad
class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    permission_classes = [IsAuthenticated]

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
        self.object.author_id = Users.objects.get(id=ad_data["author"])
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = Categories.objects.get(id=ad_data["category"])

        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "name": self.object.name,
          "author_id": self.object.author_id,
          "author": Users.objects.get(id=self.object.author_id_id).first_name,
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
            "author_id": ad.author_id,
            "author": Users.objects.get(id=ad.author_id).first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else ""
           }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
     model = Ad
     def post(self, request, *args, **kwargs):
          ad_data = json.loads(request.body)
          try:
              author_obj = Users.objects.get(id=ad_data["author_id"])
          except Users.DoesNotExist:
              return JsonResponse({"error": "Users not"}, status=404)
          try:
              category_obj = Categories.objects.get(id=ad_data["category_id"])
          except Categories.DoesNotExist:
              return JsonResponse({"error": "Categories not"}, status=404)

          ad = Ad.objects.create(
              name = ad_data["name"],
              author = author_obj,
              price = ad_data["price"],
              description = ad_data["description"],
              is_published = ad_data["is_published"],
              category = category_obj
          )

          return JsonResponse({
              "id": ad.id,
              "name": ad.name,
              "author_id": ad.author_id,
              "price": ad.price,
              "description" : ad.description,
              "is_published" : ad.is_published,
              "category_id" : ad.category_id
          }, safe=False, json_dumps_params={"ensure_ascii": True})

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
          "author": Users.objects.get(id=self.object.author_id).first_name,
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
    permission_classes = [IsAuthenticated]

class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializers

class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetaiSerializers

class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializers

class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDestroySerializers

