from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


# create superuser with given username/email/password
# and set junk values for the extended User model
# i.e. the oauth values
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email")
        parser.add_argument("username")
        parser.add_argument("password")

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.create_superuser(
            username=options["username"],
            email=options["email"],
            password=options["password"],
            rc_user_id=0,
            token_type="",
            access_token="",
            refresh_token="",
            expires_at=0,
        )
