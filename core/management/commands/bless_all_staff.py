from core.utils_rc_api import get_profile_of_rc_user_id
from core.utils_rc_profile import is_rc_profile_staff
from core.views_utils import refresh_user_token_if_needed
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("using-django-user-id")

    def handle(self, *args, **options):
        User = get_user_model()
        blessing_user_obj = User.objects.get(id=options["using-django-user-id"])

        refresh_user_token_if_needed(blessing_user_obj)

        # using single user passed above, go through all users,
        # if not already superuser, get profile, check if recurse staff, mark as superuser
        for user in User.objects.all():
            # skip existing users i.e. don't un-bless
            if user.is_superuser:
                continue

            try:
                profile = get_profile_of_rc_user_id(
                    blessing_user_obj.access_token, user.rc_user_id
                )
            except:
                print("ERROR fetching profile for user", user)
                continue

            if is_rc_profile_staff(profile):
                user.is_staff = True
                user.is_superuser = True
                user.save()
                print(f"blessed {profile['name']} as superuser")
            else:
                print(f"{profile['name']} is not recurse center staff")
