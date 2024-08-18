from allauth.account.adapter import DefaultAccountAdapter
from django.core.handlers.wsgi import WSGIRequest


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request: WSGIRequest):
        print("request path: ", request.path)
        return "/accounts/token/"
