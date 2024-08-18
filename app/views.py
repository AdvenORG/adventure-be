import ftplib
import os

import requests
from allauth.socialaccount.models import SocialToken
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.handlers.wsgi import WSGIRequest
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import redirect

from .ftp_utils import download_file
from .utils import get_tokens


def fetch_image_from_ftp(content_type_name, file_name):
    content_type = ContentType.objects.get(model=content_type_name.lower())
    remote_file_path = f"images/{content_type.model}/{file_name}"

    temp_file_path = "temp.jpg"
    download_file(remote_file_path, temp_file_path)

    with open(temp_file_path, "rb") as f:
        image_data = f.read()

    os.remove(temp_file_path)
    return image_data


def serve_ftp_image(request, content_type, file_name):
    try:
        image_data = fetch_image_from_ftp(content_type, file_name)

        if not image_data:
            raise Http404("Image not found")

        return HttpResponse(image_data, content_type="image/jpeg")
    except ftplib.all_errors:
        raise Http404("Image not found")


def keycloak_callback(request):
    print(request)
    auth_code = request.GET.get("code")
    if not auth_code:
        return HttpResponseBadRequest("Missing authorization code")

    try:
        tokens = get_tokens(auth_code)
    except Exception as e:
        return HttpResponseBadRequest(str(e))

    access_token = tokens["access_token"]
    user_info_url = f"{settings.KEYCLOAK_BASE_URL}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens.get("refresh_token")
    request.session["id_token"] = tokens.get("id_token")
    if user_info_response.status_code != 200:
        return HttpResponseBadRequest("Failed to fetch user info")

    user_info = user_info_response.json()

    # Store tokens and user info in session
    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens.get("refresh_token")
    request.session["id_token"] = tokens.get("id_token")
    request.session["user_info"] = user_info

    return redirect("/auth/intermediate/")


def token(request: WSGIRequest):
    try:
        token = SocialToken.objects.get(
            account__user=request.user, account__provider="keycloak"
        )
    except SocialToken.DoesNotExist as e:
        return HttpResponseBadRequest(f"Can't handle request for {request.user}")

    data = {
        "access_token": token.token,
        "refresh_token": token.token_secret,
        "expires_at": token.expires_at,
    }
    token.delete()
    return JsonResponse(data)


def my_protected_api_view(request: HttpRequest):
    # Retrieve the access token from the headers
    access_token = request.headers.get("Authorization")

    if not access_token:
        return HttpResponseForbidden("Access token is missing or expired")
    # Set up the headers with the access token
    headers = {
        "Authorization": access_token,
    }
    user_info_url = f"{settings.KEYCLOAK_BASE_URL}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    if user_info_response.status_code == 200:
        # Return the response from the external API as JSON
        return JsonResponse(user_info_response.json())
    else:
        # Handle error responses from the external API
        return HttpResponseBadRequest("Failed to fetch data from external API")
