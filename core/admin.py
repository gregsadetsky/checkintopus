import re

import requests
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path

from .models import RFIDTagScanLog, Sound, User
from .utils_rc_api import get_batches, get_profile, get_profiles_by_batch_id
from .utils_rc_profile import get_latest_batch_name
from .views_utils import refresh_user_token_if_needed

admin.site.site_title = "Octopass"
admin.site.site_header = "Octopass admin"
admin.site.index_template = "admin/index_custom.html"


class MyUserAdmin(UserAdmin):
    change_form_template = "loginas/change_form.html"
    list_display = (
        "username",
        "rfid_tag_fc",
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
            return "*** error fetching info! ***"

        try:
            user_profile = get_profile(user.access_token)
        except:
            print("ERROR getting profile for user", user)
            return "*** error fetching info! ***"

        batch_name = get_latest_batch_name(user_profile)
        if batch_name:
            return f"{user_profile['name']} ({batch_name})"

        return user_profile["name"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "pre_register_rfid_tags/",
                self.admin_site.admin_view(self.pre_register_rfid_tags_pick_batch),
                name="pre_register_rfid_tags_pick_batch",
            ),
            path(
                "pre_register_rfid_tags/batch/<str:batch_id>/",
                self.admin_site.admin_view(self.pre_register_rfid_tags_pick_user),
                name="pre_register_rfid_tags_pick_user",
            ),
        ]
        return my_urls + urls

    def pre_register_rfid_tags_pick_batch(self, request):
        if request.method == "POST":
            batch_id = request.POST["batch_id"]
            return redirect("admin:pre_register_rfid_tags_pick_user", batch_id)

        assert request.method == "GET"

        batches = get_batches(request.user.access_token)
        batches = sorted(batches, key=lambda b: b["start_date"], reverse=True)

        context = dict(
            self.admin_site.each_context(request),
            batches=batches,
        )
        return TemplateResponse(
            request, "admin/core/user/pre_register_rfid_tags_pick_batch.html", context
        )

    def pre_register_rfid_tags_pick_user(self, request, batch_id):
        if request.method == "POST":
            rc_user_id = request.POST["rc_user_id"]
            scanned_rfid_tag = request.POST["scanned_rfid_tag"]
            # check that it's in the format that expect
            if re.match(r"^\d+-\d+$", scanned_rfid_tag) is None:
                messages.error(
                    request,
                    "Invalid format for scanned rfid tag. Expected format: '1234-5678'",
                )
            else:
                tag_fc, tag_id = scanned_rfid_tag.split("-")
                user, _ = User.objects.update_or_create(
                    rc_user_id=rc_user_id,
                    defaults={
                        "username": f"rc-{rc_user_id}",
                        "rfid_tag_fc": tag_fc,
                        "rfid_tag_card": tag_id,
                    },
                )
                messages.success(
                    request,
                    f"Saved rfid tag {scanned_rfid_tag} for RC user {rc_user_id}",
                )

        profiles = get_profiles_by_batch_id(request.user.access_token, batch_id)
        profiles = sorted(profiles, key=lambda p: p["name"])

        context = dict(
            self.admin_site.each_context(request),
            profiles=profiles,
        )
        return TemplateResponse(
            request, "admin/core/user/pre_register_rfid_tags_pick_user.html", context
        )


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
