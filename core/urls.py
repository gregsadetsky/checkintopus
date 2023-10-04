from django.urls import path

from .views import index, oauth_redirect
from .views_helpers import (
    add_community_sound,
    all_community_sounds_view,
    delete_community_sound,
    sound_preferences,
)
from .views_onboarding import onboarding, onboarding_confirm_card
from .views_scan import scan

urlpatterns = [
    path("", index, name="index"),
    path("onboarding", onboarding, name="onboarding"),
    path(
        "onboarding/confirm_card",
        onboarding_confirm_card,
        name="onboarding_confirm_card",
    ),
    # oauth redirect from recurse allowing us to get an access token
    path("oauth_redirect", oauth_redirect, name="oauth_redirect"),
    # pings from the rfid scanner/raspberry pi
    path("api/scan", scan, name="scan"),
    path("sound_preferences", sound_preferences, name="sound_preferences"),
    path(
        "all_community_sounds", all_community_sounds_view, name="all_community_sounds"
    ),
    path("add_community_sound", add_community_sound, name="add_community_sound"),
    path(
        "delete_community_sound", delete_community_sound, name="delete_community_sound"
    ),
]
