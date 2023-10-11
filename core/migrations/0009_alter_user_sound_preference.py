# Generated by Django 4.2.5 on 2023-10-05 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_rfidtagscanlog_options_alter_sound_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="sound_preference",
            field=models.CharField(
                choices=[
                    ("no_sound", "no sound"),
                    ("single_sound", "a single sound"),
                    ("random_community_sound", "a random community sound"),
                ],
                default="random_community_sound",
                max_length=100,
            ),
        ),
    ]