from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RFIDTagScanLog, Sound, User


class MyUserAdmin(UserAdmin):
    change_form_template = "loginas/change_form.html"


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
