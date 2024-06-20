from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from . import views
from .views import serve_ftp_image

admin.site.site_title = "Adventure"
admin.site.site_header = "Adventure CMS"
admin.site.index_title = "Admin"


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/oidc/keycloak/login/callback/",
        views.keycloak_callback,
        name="keycloak_callback",
    ),
    path("auth/intermediate/", views.intermediate, name="intermediate"),
    path("profile/", views.profile, name="profile"),
    path("accounts/", include("allauth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "api/",
        include(
            [
                path("store/", include("store.urls")),
            ]
        ),
    ),
    path(
        "images/<str:content_type>/<str:file_name>",
        serve_ftp_image,
        name="serve_ftp_image",
    ),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
