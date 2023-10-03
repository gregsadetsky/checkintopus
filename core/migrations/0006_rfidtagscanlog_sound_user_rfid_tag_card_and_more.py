# Generated by Django 4.2.5 on 2023-10-02 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_delete_oauth2token_user_access_token_user_expires_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="RFIDTagScanLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("scan_time", models.DateTimeField(auto_now_add=True)),
                ("rfid_tag_fc", models.CharField(max_length=100)),
                ("rfid_tag_card", models.CharField(max_length=100)),
                (
                    "unknown_card_random_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sound",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="community_sounds/")),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="rfid_tag_card",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="rfid_tag_fc",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="sound_preference",
            field=models.CharField(
                choices=[
                    ("no_sound", "no sound"),
                    ("single_sound", "single sound"),
                    ("random_community_sound", "random community sound"),
                ],
                default="random_community_sound",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="single_sound_preference",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.sound",
            ),
        ),
    ]
