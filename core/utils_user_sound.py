from .models import Sound


def get_sound_url_for_user(user):
    if user.sound_preference == "no_sound":
        return None
    elif user.sound_preference == "single_sound":
        return user.single_sound_preference.file.url
    elif user.sound_preference == "random_community_sound":
        return Sound.objects.order_by("?").first().file.url

    raise Exception("invalid sound_preference")
