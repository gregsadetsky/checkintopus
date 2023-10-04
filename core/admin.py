from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RFIDTagScanLog, Sound, User

admin.site.register(User, UserAdmin)


class RFIDTagScanLogAdmin(admin.ModelAdmin):
    list_display = (
        "scan_time",
        "rfid_tag_fc",
        "rfid_tag_card",
        "unknown_card_random_name",
    )


admin.site.register(RFIDTagScanLog, RFIDTagScanLogAdmin)
admin.site.register(Sound)
