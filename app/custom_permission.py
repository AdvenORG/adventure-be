from rest_framework.permissions import BasePermission
from django.conf import settings
import requests
from rest_framework.exceptions import APIException

class KeycloakProtectedPermission(BasePermission):
    def has_permission(self, request, view):
        access_token = request.headers.get("Authorization")
        if not access_token:
            raise APIException("Access token is missing or expired", code=403)

        user_info_url = f"{settings.KEYCLOAK_BASE_URL}/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code == 200:
            request.user_info = user_info_response.json()
            return True
        else:
            raise APIException("Failed to fetch data from external API", code=400)
