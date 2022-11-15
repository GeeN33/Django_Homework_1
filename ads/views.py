import json
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, response, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from ads.models import Ad, Categories, Users, Location



def index(request):
    if request.method == "GET":
        return JsonResponse({"status": "ok"}, safe=False, status=200)
# Users
class UsersListView(ListView):
    model = Users
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # self.object_list = self.object_list.order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(user.location_id.all().values_list("name", flat=True))
            })
        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": True})

class UsersDetailView(DetailView):
    model = Users
    def get(self, request, *args, **kwargs):
        try:
            user = Users.objects.get(pk=kwargs['pk'])
        except Users.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the user"}, status=404)

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.password,
            "role": user.role,
            "age": user.age,
            "locations": list(user.location_id.all().values_list("name", flat=True))
           }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class UsersCreateView(CreateView):
     model = Users
     def post(self, request, *args, **kwargs):
          user_data = json.loads(request.body)

          user = Users.objects.create(
               username=user_data["username"],
               password=user_data["password"],
               first_name=user_data["first_name"],
               last_name=user_data["last_name"],
               role= user_data["role"],
               age=user_data["age"],
          )

          for location in user_data["locations"]:
               try:
                    location_obj = Location.objects.get(name=location)
               except Location.DoesNotExist:
                    return JsonResponse({"error": "Location not"}, status=404)

               user.location_id.add(location_obj)

          return JsonResponse({
              "id": user.id,
              "username": user.username,
              "first_name": user.first_name,
              "last_name": user.last_name,
              "role": user.role,
              "age": user.age,
              "locations": list(user.location_id.all().values_list("name", flat=True))
          }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class UsersUpdateView(UpdateView):
    model = Users
    fields = ["username", "password", "first_name", "last_name", "username", "age", "location_id"]
    def patch(self, request, *args, **kwargs):
        try:
             Users.objects.get(pk=kwargs['pk'])
        except Users.DoesNotExist:
             return JsonResponse({"error": "there is no such id in the user"}, status=404)
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.age = user_data["age"]

        for location in user_data["locations"]:
           try:
                location_obj = Location.objects.get(name=location)
           except Location.DoesNotExist:
                return JsonResponse({"error": "Location not"}, status=404)

           self.object.location_id.add(location_obj)

        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "username": self.object.username,
          "first_name": self.object.first_name,
          "last_name": self.object.last_name,
          "age": self.object.age,
          "locations": list(self.object.location_id.all().values_list("name", flat=True))
        }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class UsersDeleteView(DeleteView):
     model = Users
     success_url = '/'
     def delete(self, request, *args, **kwargs):
         try:
             Users.objects.get(pk=kwargs['pk'])
         except Users.DoesNotExist:
             return JsonResponse({"error": "there is no such id in the user"}, status=404)

         super().delete( request, *args, **kwargs)
         return JsonResponse({"status": "ok"}, status=200)

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
                "locations": list(user.location_id.all().values_list("name", flat=True)),
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

# Categories
@method_decorator(csrf_exempt, name="dispatch")
class CatListView(ListView):
    model = Categories
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        response = []
        for cat in self.object_list:
            response.append({
                "id": cat.id,
                "name": cat.name
            })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": True})

class CatDetailView(DetailView):
    model = Categories
    def get(self, request, *args, **kwargs):
            try:
                category = self.get_object()
            except :
                return JsonResponse({"error": "there is no such id in the category"}, status=404)

            return JsonResponse({
                    "id": category.id,
                    "name": category.name
                }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(CreateView):
     model = Categories
     def post(self, request, *args, **kwargs):
          cat_data = json.loads(request.body)

          cat = Categories.objects.create(
               name=cat_data["name"]
          )

          return JsonResponse({
              "id": cat.id,
              "name": cat.name
          }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class CatUpdateView(UpdateView):
    model = Categories
    fields = ["name"]
    def patch(self, request, *args, **kwargs):
        try:
            Categories.objects.get(pk=kwargs['pk'])
        except Categories.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the cat"}, status=404)
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data["name"]
        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "name": self.object.name
        }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class CatDeleteView(DeleteView):
     model = Categories
     success_url = '/'
     def delete(self, request, *args, **kwargs):
         try:
             Categories.objects.get(pk=kwargs['pk'])
         except Categories.DoesNotExist:
             return JsonResponse({"error": "there is no such id in the cat"}, status=404)

         super().delete( request, *args, **kwargs)
         return JsonResponse({"status": "ok"}, status=200)

#Ad
class AdListView(ListView):
    model = Ad
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ad = []
        for a in page_obj:
            ad.append({
                "id": a.id,
                "name": a.name,
                "author_id": a.author_id_id,
                "author": Users.objects.get(id=a.author_id_id).first_name,
                "price": a.price,
                "description": a.description,
                "is_published": a.is_published,
                "category_id": a.category_id_id,
                "image":  a.image.url if a.image else ""
            })
        response = {
            "items": ad,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": True})

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
        self.object.author_id = Users.objects.get(id=ad_data["author_id"])
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = Categories.objects.get(id=ad_data["category_id"])

        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "name": self.object.name,
          "author_id": self.object.author_id_id,
          "author": Users.objects.get(id=self.object.author_id_id).first_name,
          "price": self.object.price,
          "description": self.object.description,
          "is_published": self.object.is_published,
          "category_id": self.object.category_id_id,
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
            "author_id": ad.author_id_id,
            "author": Users.objects.get(id=ad.author_id_id).first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id_id,
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
              author_id = author_obj,
              price = ad_data["price"],
              description = ad_data["description"],
              is_published = ad_data["is_published"],
              category_id = category_obj
          )

          return JsonResponse({
              "id": ad.id,
              "name": ad.name,
              "author_id": ad.author_id_id,
              "price": ad.price,
              "description" : ad.description,
              "is_published" : ad.is_published,
              "category_id" : ad.category_id_id
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
          "author_id": self.object.author_id_id,
          "author": Users.objects.get(id=self.object.author_id_id).first_name,
          "price": self.object.price,
          "description": self.object.description,
          "is_published": self.object.is_published,
          "category_id": self.object.category_id_id,
          "image": self.object.image.url if self.object.image else None

        }, safe=False, json_dumps_params={"ensure_ascii": True})