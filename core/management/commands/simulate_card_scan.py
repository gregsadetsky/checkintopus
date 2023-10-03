import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("server_url")
        parser.add_argument("fc")
        parser.add_argument("card")

    def handle(self, *args, **options):
        r = requests.post(
            f'{options["server_url"]}{reverse("scan")}',
            headers={"x-api-key": settings.RASPI_SCAN_UUID_API_KEY},
            json={"fc": options["fc"], "card": options["card"]},
        )
        assert r.json()
        print(json.dumps(r.json(), indent=4))
