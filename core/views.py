import json

from authlib.integrations.django_client import OAuth, OAuthError
from django.conf import settings
from django.contrib import messages
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


# decorator -- require oauth authentication
def oauth_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return rc_oauth.authorize_redirect(request, settings.RC_OAUTH_REDIRECT_URI)

        try:
            # check that token is valid by making an api request
            _ = get_profile(request.user.access_token)
        except UnauthorizedError:
            request.user.delete()
            logout(request)
            return redirect("index")

        return func(request, *args, **kwargs)

    return wrapper


@oauth_required
def index(request):
    all_community_sounds = Sound.objects.all()
    rc_profile = get_profile(request.user.access_token)

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


@oauth_required
def all_community_sounds(request):
    all_community_sounds = Sound.objects.all()
    return render(
        request,
        "core/all_community_sounds.html",
        {"all_community_sounds": all_community_sounds},
    )


@oauth_required
def sound_preferences(request):
    if request.method == "POST":
        # load values from submitted forms
        # <select name='sound-preference'> and
        # <select name='single-sound-preference'>
        sound_preference = request.POST.get("sound-preference")
        single_sound_preference = request.POST.get("single-sound-preference")

        request.user.sound_preference = sound_preference

        if sound_preference == "single_sound":
            request.user.single_sound_preference = Sound.objects.get(
                id=single_sound_preference
            )
        else:
            request.user.single_sound_preference = None
        request.user.save()

        messages.success(request, "saved!")

        # redirect to avoid back-reload-resubmit issues
        return redirect("sound_preferences")

    all_community_sounds = Sound.objects.all()
    return render(
        request,
        "core/sound_preferences.html",
        {"all_community_sounds": all_community_sounds},
    )


@oauth_required
def add_community_sound(request):
    if request.method == "POST":
        # get file from <input name="file"/>
        file = request.FILES["file"]
        # create new sound object
        Sound.objects.create(
            file=file,
        )

        messages.success(request, "sound added!")

        # redirect to avoid back-reload-resubmit issues
        return redirect("add_community_sound")

    return render(request, "core/add_community_sound.html")


@oauth_required
def delete_community_sound(request):
    if request.method == "POST":
        sound_id = request.POST.get("sound")

        sound_obj = Sound.objects.get(id=sound_id)

        # find all users that have a 'sound_preference' of 'single_sound' and this sound set as 'single_sound_preference'
        # and set their single_sound_preference to none and their preference to 'random_community_sound'
        users_with_single_sound_preference = User.objects.filter(
            sound_preference="single_sound",
            single_sound_preference=sound_obj,
        )
        for user in users_with_single_sound_preference:
            user.sound_preference = "random_community_sound"
            user.single_sound_preference = None
            user.save()

        # delete file
        sound_obj.file.delete()
        sound_obj.delete()

        messages.success(request, "sound deleted!")

        # redirect to avoid back-reload-resubmit issues
        return redirect("delete_community_sound")

    all_community_sounds = Sound.objects.all()
    return render(
        request,
        "core/delete_community_sound.html",
        {"all_community_sounds": all_community_sounds},
    )
