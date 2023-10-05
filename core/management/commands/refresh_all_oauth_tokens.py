from core.models import User
from core.views_utils import refresh_user_token_if_needed
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        # go through all User that have an access_token
        # and call refresh_user_token_if_needed on them

        for user in User.objects.filter(access_token__isnull=False):
            refresh_user_token_if_needed(user)
