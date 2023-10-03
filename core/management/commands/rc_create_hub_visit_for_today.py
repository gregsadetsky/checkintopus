import json

from core.utils_rc_api import create_hub_visit_for_today
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("rc_user_id")

    def handle(self, *args, **options):
        User = get_user_model()
        user_obj = User.objects.get(rc_user_id=options["rc_user_id"])

        print(
            json.dumps(
                create_hub_visit_for_today(user_obj.access_token, user_obj.rc_user_id),
                indent=4,
            )
        )
