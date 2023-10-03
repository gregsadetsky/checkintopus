from django.urls import path

from core.views import index, oauth_redirect
from core.views_scan import scan

urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    path("oauth_redirect", oauth_redirect, name="oauth_redirect"),
    path("api/scan", scan, name="scan"),
]
