# custom handler
import requests
from django.conf import settings
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.default_code

    return response


def get_tokens(auth_code):
    token_url = f"{settings.KEYCLOAK_BASE_URL}/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": settings.KEYCLOAK_REDIRECT_URI,
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to fetch tokens: {response.status_code} {response.text}"
        )
