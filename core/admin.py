from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RFIDTagScanLog, Sound, User
from .utils_rc_api import get_profile
from .utils_rc_profile import get_latest_batch_name
from .views_utils import refresh_user_token_if_needed

admin.site.site_title = "Octopass"
admin.site.site_header = "Octopass admin"


class MyUserAdmin(UserAdmin):
    change_form_template = "loginas/change_form.html"
    list_display = (
        "username",
        "rfid_tag_card",
        "is_superuser",
        "get_name_for_user",
    )

    @admin.display(description="Name")
    def get_name_for_user(self, user):
        if not user.access_token:
            return ""

        try:
            # weird things can happen if the access token is not valid anymore
            # but we still store it in the db
            refresh_user_token_if_needed(user)
        except:
            print("ERROR refreshing token for user", user)
            return "(error fetching info)"

        try:
            user_profile = get_profile(user.access_token)
        except:
            print("ERROR getting profile for user", user)
            return "(error fetching info)"

        batch_name = get_latest_batch_name(user_profile)
        if batch_name:
            return f"{user_profile['name']} ({batch_name})"

        return user_profile["name"]


admin.site.register(User, MyUserAdmin)


class RFIDTagScanLogAdmin(admin.ModelAdmin):
    list_display = (
        "scan_time",
        "rfid_tag_fc",
        "rfid_tag_card",
        "unknown_card_random_name",
    )


admin.site.register(RFIDTagScanLog, RFIDTagScanLogAdmin)
admin.site.register(Sound)
