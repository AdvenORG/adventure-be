# decorators.py

import requests
from django.conf import settings
from django.http import JsonResponse


def token_auth_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Retrieve the access token from the request headers
        access_token = (
            request.headers.get("Authorization", "").split("Bearer ")[-1].strip()
        )

        if not access_token:
            return JsonResponse(
                {"error": "Authorization header missing or invalid"}, status=403
            )

        # Validate the access token (optional, you may need to adjust based on your setup)
        user_info_url = f"{settings.KEYCLOAK_BASE_URL}/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(user_info_url, headers=headers)

        if response.status_code != 200:
            return JsonResponse({"error": "Invalid access token"}, status=403)

        # Add token info to request object if needed
        user_info = response.json()
        request.session["user_info"] = user_info
 
        # Call the view function
        return view_func(request, *args, **kwargs)

    return wrapped_view
