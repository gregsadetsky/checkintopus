from django.urls import path

from core.views import (
    add_community_sound,
    all_community_sounds,
    delete_community_sound,
    index,
    oauth_redirect,
    sound_preferences,
)
from core.views_scan import scan

urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    # oauth redirect from recurse allowing us to get an access token
    path("oauth_redirect", oauth_redirect, name="oauth_redirect"),
    # pings from the rfid scanner/raspberry pi
    path("api/scan", scan, name="scan"),
    path("sound_preferences", sound_preferences, name="sound_preferences"),
    path("all_community_sounds", all_community_sounds, name="all_community_sounds"),
    path("add_community_sound", add_community_sound, name="add_community_sound"),
    path(
        "delete_community_sound", delete_community_sound, name="delete_community_sound"
    ),
]
