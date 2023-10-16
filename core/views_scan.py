import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import RFIDTagScanLog
from .utils_onboarding_sound_urls import generate_onboarding_sound_urls_for_card
from .utils_rc_api import create_hub_visit_for_today
from .utils_user_sound import get_sound_url_for_user
from .utils_uuid import check_that_string_is_uuid
from .views_utils import refresh_user_token_if_needed


@require_http_methods(["POST"])
@csrf_exempt
def scan(request):
    API_KEY = request.headers["x-api-key"]

    # sanity checks
    assert len(API_KEY) == len(settings.RASPI_SCAN_UUID_API_KEY) == 36
    assert check_that_string_is_uuid(API_KEY)

    if API_KEY != settings.RASPI_SCAN_UUID_API_KEY:
        return JsonResponse({"error": "invalid API key"}, status=401)

    # get json body
    body = json.loads(request.body.decode("utf-8"))
    fc = str(body["fc"])
    card = str(body["card"])

    assert fc and len(fc) > 0
    assert card and len(card) > 0

    # log visit
    rfid_tag_scan_log_object = RFIDTagScanLog(
        rfid_tag_fc=fc,
        rfid_tag_card=card,
    )
    rfid_tag_scan_log_object.save()

    # two possible scenarios:
    # - we know who the user is -- play their sound, ping the hubs visit api
    # - we don't know who the user is -- direct them to the onboarding

    # is there a user with this fc/card?
    User = get_user_model()
    found_user = User.objects.filter(
        rfid_tag_fc=fc,
        rfid_tag_card=card,
    ).first()

    if found_user:
        # we'll get back one sound, so make it a list of 1
        found_sound = get_sound_url_for_user(found_user)
        # found_sound will be None for users who opt for no sound!
        sound_urls = [found_sound] if found_sound else []

        # important! possibly refresh token as access_token goes stale pretty fast
        refresh_user_token_if_needed(found_user)

        create_hub_visit_for_today(found_user.access_token, found_user.rc_user_id)
    else:
        # onboarding will return multiple urls - onboarding message + color + fruit
        res = generate_onboarding_sound_urls_for_card(fc, card)
        sound_urls = res["sound_urls"]
        random_color_fruit_string = res["random_color_fruit_string"]

        # assign a random color+fruit name to the card that was just scanned
        # we 'send back' the name of this color+fruit in audio format, which the user will hear;
        # then, they can go to the onboarding web ui to setup their account and associate
        # the card (which they just scanned) with their account
        rfid_tag_scan_log_object.unknown_card_random_name = random_color_fruit_string
        rfid_tag_scan_log_object.save()

    return JsonResponse(
        {
            "sound_urls": sound_urls,
        }
    )
