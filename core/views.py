from authlib.integrations.django_client import OAuthError
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Sound, User
from .utils_rc_api import get_profile
from .views_utils import get_rc_oauth, oauth_required


@oauth_required
def index(request, rc_profile):
    if not request.user.has_user_card_been_onboarded():
        return redirect("onboarding")

    all_community_sounds = Sound.objects.all()

    return render(
        request,
        "core/index.html",
        {"rc_profile": rc_profile, "all_community_sounds": all_community_sounds},
    )


def oauth_redirect(request):
    # TODO the call below can fail -- fail hard? show an error?
    try:
        token = get_rc_oauth().authorize_access_token(request)
    except OAuthError as exception:
        if exception.error == "access_denied":
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
