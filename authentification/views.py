from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import  ListView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from Django_Homework_1 import settings
from authentification.models import User
from authentification.serializers import UsersSerializers, UsersCreateSerializers,\
    UsersUpdateSerializers, UsersDestroySerializers

# class UserCreateView(CreateAPIView):
#     model = User
#     serializer_class = UserCreateSerializer

class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializers

class UsersDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializers

class UsersCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateSerializers

class UsersUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersUpdateSerializers

class UsersDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersDestroySerializers

class UsersZView(ListView):
    model = User

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

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


def obtain_auth_token(request):
    return None