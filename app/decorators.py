# import requests
# from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
# from functools import wraps
# from django.conf import settings

# def keycloak_protected(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         # Retrieve the access token from the headers
#         access_token = request.headers.get("Authorization")

#         if not access_token:
#             return HttpResponseForbidden("Access token is missing or expired")

#         # Set up the headers with the access token
#         user_info_url = f"{settings.KEYCLOAK_BASE_URL}/userinfo"
#         headers = {"Authorization": f"Bearer {access_token}"}
#         user_info_response = requests.get(user_info_url, headers=headers)

#         if user_info_response.status_code == 200:
#             request.user_info = user_info_response.json()
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseBadRequest("Failed to fetch data from external API")

#     return _wrapped_view
