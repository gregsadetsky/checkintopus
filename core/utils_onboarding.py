import random

from django.core.files.storage import default_storage

ONBOARDING_S3_FILE_PATH = "onboarding/welcome.mp3"
COLOR_AND_FRUITS_S3_DIR = "onboarding/colors-and-fruits"

COLORS = [
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "pink",
    "brown",
    "black",
    "white",
]

FRUITS = [
    "apple",
    "banana",
    "cherry",
    "grape",
    "kiwi",
    "lemon",
    "lime",
    "mango",
    "peach",
]


def generate_onboarding_sound_urls_for_card(fc, card):
    # signs the url and everything! crazy useful!
    onboarding_s3_url = default_storage.url(ONBOARDING_S3_FILE_PATH)

    sound_urls = [onboarding_s3_url]

    random_color = random.choice(COLORS)
    random_fruit = random.choice(FRUITS)

    for sound_name in [random_color, random_fruit]:
        sound_urls.append(
            default_storage.url(f"{COLOR_AND_FRUITS_S3_DIR}/{sound_name}.mp3")
        )

    return {
        "sound_urls": sound_urls,
        "random_color_fruit_string": f"{random_color} {random_fruit}",
    }
