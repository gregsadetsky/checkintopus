from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RFIDTagScanLog, Sound, User

admin.site.register(User, UserAdmin)

admin.site.register(RFIDTagScanLog)
admin.site.register(Sound)
