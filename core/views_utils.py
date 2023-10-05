from datetime import datetime

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

from .models import User
from .utils_rc_api import UnauthorizedError, get_profile


def get_rc_oauth():
    rc_oauth = OAuth().register(
        "Recurse Center",
        api_base_url="https://www.recurse.com/api/v1/",
        authorize_url="https://www.recurse.com/oauth/authorize",
        access_token_url="https://www.recurse.com/oauth/token",
        client_id=settings.RC_OAUTH_APP_ID,
        client_secret=settings.RC_OAUTH_APP_SECRET,
    )
    assert rc_oauth is not None
    return rc_oauth


def refresh_user_token_if_needed(user):
    utc_timestamp = datetime.now().timestamp()

    # has the oauth token expired?
    if user.expires_at < utc_timestamp:
        # refresh it
        token = get_rc_oauth().fetch_access_token(
            "https://www.recurse.com/oauth/token",
            grant_type="refresh_token",
            refresh_token=user.refresh_token,
        )
        user.access_token = token["access_token"]
        user.refresh_token = token["refresh_token"]
        user.expires_at = token["expires_at"]
        user.save()


# decorator -- require oauth authentication
def oauth_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return get_rc_oauth().authorize_redirect(
                request, settings.RC_OAUTH_REDIRECT_URI
            )

        refresh_user_token_if_needed(request.user)

        try:
            # check that token is valid by making an api request
            rc_profile = get_profile(request.user.access_token)
        except UnauthorizedError:
            request.user.delete()
            logout(request)
            return redirect("index")

        # inject rc_profile into the kwargs
        # any wrapped function (right now, just the index view) will get it for free
        # i.e. won't need to do the api call itself (slowing the server's response)
        kwargs["rc_profile"] = rc_profile
        return func(request, *args, **kwargs)

    return wrapper


# simpler wrapper that makes sure that user is logged in
# this doesn't check that the access token is still valid;
# you'd use it for views that presumably don't take actions
# on the user's behalf that would require a token
# (those actions will fail if the token is invalid regardless of
# whether we check it here)
def authentication_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("index")

        return func(request, *args, **kwargs)

    return wrapper
