from rest_framework import permissions
from .models import Client
from .utils.auth import hash_api_key


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        raw_api_key = request.META.get('HTTP_API_KEY', '')

        return Client.objects.filter(api_key=hash_api_key(raw_api_key)).exists()
