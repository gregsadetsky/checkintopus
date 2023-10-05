import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    rc_user_id = models.PositiveIntegerField(unique=True)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    # TODO should be renamed to access_token_expires_at to make it clearer!
    expires_at = models.PositiveIntegerField()

    rfid_tag_fc = models.CharField(max_length=100, blank=True)
    # TODO rename to rfid_tag_card_id
    rfid_tag_card = models.CharField(max_length=100, blank=True)

    SOUND_PREFERENCE_CHOICES = [
        ("no_sound", "no sound"),
        ("single_sound", "a single sound"),
        ("random_community_sound", "a random community sound"),
    ]
    sound_preference = models.CharField(
        max_length=100,
        choices=SOUND_PREFERENCE_CHOICES,
        default="random_community_sound",
    )
    single_sound_preference = models.ForeignKey(
        "Sound",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def has_user_card_been_onboarded(self):
        return self.rfid_tag_fc and self.rfid_tag_card


class RFIDTagScanLog(models.Model):
    scan_time = models.DateTimeField(auto_now_add=True)

    rfid_tag_fc = models.CharField(max_length=100)
    # TODO rename to rfid_tag_card_id
    rfid_tag_card = models.CharField(max_length=100)

    # when an unknown card is scanned, a random name is generated from it and sent back
    # to the user in the audio message.
    # during onboarding, the user can find the random name they were told in the list of 'unclaimed' cards.
    unknown_card_random_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["-scan_time"]


class Sound(models.Model):
    file = models.FileField(upload_to="community_sounds/")

    class Meta:
        ordering = ["file"]

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.filename
