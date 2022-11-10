import json
from django.http import JsonResponse, response
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ads, Categories

def index(request):
    if request.method == "GET":
        return JsonResponse({"status": "ok"}, safe=False, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):
    def post(self, request):
            ad_data = json.loads(request.body)
            ad = Ads()
            ad.name = ad_data["name"]
            ad.author = ad_data["author"]
            ad.price = ad_data["price"]
            ad.description = ad_data["description"]
            ad.address = ad_data["address"]
            ad.is_published = ad_data["is_published"]
            ad.save()
            return JsonResponse({
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published
               }, safe=False, json_dumps_params={"ensure_ascii": True})

    def get(self, request):
            ads = Ads.objects.all()
            response = []
            for ad in ads:
                response.append({
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published
                })
            return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": True})

class AdDetailView(DetailView):
    model = Ads
    def get(self, request, *args, **kwargs):

        try:
            ad = self.get_object()
        except:
            return JsonResponse({"error": "there is no such id in the ads"}, status=404)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
           }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class CatView(View):
    def post(self, request):
        category_data = json.loads(request.body)
        category = Categories()
        category.name = category_data["name"]
        category.save()
        return JsonResponse({
                "id": category.id,
                "name": category.name
            }, safe=False, json_dumps_params={"ensure_ascii": True})

    def get(self, request):
        categories = Categories.objects.all()
        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name
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