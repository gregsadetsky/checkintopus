from django.urls import path

from core.views import index, oauth_redirect

urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    path("oauth_redirect", oauth_redirect, name="oauth_redirect"),
]
