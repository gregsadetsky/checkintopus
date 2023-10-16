import json

from core.utils_rc_api import get_profile_of_rc_user_id
from core.views_utils import refresh_user_token_if_needed
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("get-rc-profile-id")
        parser.add_argument("using-django-user-id")

    def handle(self, *args, **options):
        User = get_user_model()
        user_obj = User.objects.get(id=options["using-django-user-id"])

        refresh_user_token_if_needed(user_obj)
        print(
            json.dumps(
                get_profile_of_rc_user_id(
                    user_obj.access_token, options["get-rc-profile-id"]
                ),
                indent=4,
            )
        )
