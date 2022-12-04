from django.http import JsonResponse
from rest_framework import permissions

from ads.models import Selection
from authentification.models import User


class SelectionPermission(permissions.BasePermission):
    message = 'User not owner!'

    def has_permission(self, request, view):
        r = request.data['owner']

        u = request.user.id

        if r != u:
            return False
        return True

class SelectionDeletePermission(permissions.BasePermission):
    message = 'User not owner!'

    def has_permission(self, request, view):

        owner = 0
        try:
            owner = Selection.objects.get(pk = view.kwargs['pk']).owner
        except Selection.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the Selection"}, status=404)

        u = request.user.id


        if owner != u:
            return False
        return True

