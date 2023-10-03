import json

from authlib.integrations.django_client import OAuth, OAuthError
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Sound, User
from .utils_rc_api import UnauthorizedError, get_profile

rc_oauth = OAuth().register(
    "Recurse Center",
    api_base_url="https://www.recurse.com/api/v1/",
    authorize_url="https://www.recurse.com/oauth/authorize",
    access_token_url="https://www.recurse.com/oauth/token",
    client_id=settings.RC_OAUTH_APP_ID,
    client_secret=settings.RC_OAUTH_APP_SECRET,
)


def index(request):
    # check if user is not anonymous
    if not request.user.is_authenticated:
        return rc_oauth.authorize_redirect(request, settings.RC_OAUTH_REDIRECT_URI)

    try:
        rc_profile = get_profile(request.user.access_token)
    except UnauthorizedError:
        request.user.delete()
        logout(request)
        return redirect("index")

    all_community_sounds = Sound.objects.filter().order_by("name")

    return render(
        request,
        "core/index.html",
        {"rc_profile": rc_profile, "all_community_sounds": all_community_sounds},
    )


def oauth_redirect(request):
    # TODO the call below can fail -- fail hard? show an error?
    try:
        token = rc_oauth.authorize_access_token(request)
    except OAuthError as e:
        if e.error == "access_denied":
            return HttpResponse(
                b"""looks like you denied access, that's ok. <a href="/">want to try again?</a>"""
            )
        raise

    profile = get_profile(token["access_token"])
    rc_user_id = profile["id"]

    # create/re-save the tokens in the db
    user, _ = User.objects.update_or_create(
        rc_user_id=rc_user_id,
        defaults={
            "username": f'rc-{profile["id"]}',
            "token_type": token["token_type"],
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "expires_at": token["expires_at"],
        },
    )

    login(request, user)

    # redirect back to the home
    return redirect("index")
