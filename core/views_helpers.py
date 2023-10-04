from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Sound, User
from .views_utils import authentication_required


# bit of a different view name to avoid conflicting
# with 'all_community_sounds' variable
@authentication_required
def all_community_sounds_view(request):
    all_community_sounds = Sound.objects.all()
    return render(
        request,
        "core/all_community_sounds.html",
        {"all_community_sounds": all_community_sounds},
    )


@authentication_required
def sound_preferences(request):
    if request.method == "POST":
        # load values from submitted forms
        # <select name='sound-preference'> and
        # <select name='single-sound-preference'>
        sound_preference = request.POST.get("sound-preference")
        single_sound_preference = request.POST.get("single-sound-preference")

        request.user.sound_preference = sound_preference

        if sound_preference == "single_sound":
            request.user.single_sound_preference = Sound.objects.get(
                id=single_sound_preference
            )
        else:
            request.user.single_sound_preference = None
        request.user.save()

        messages.success(request, "saved!")

        # redirect to avoid back-reload-resubmit issues
        return redirect("sound_preferences")

    all_community_sounds = Sound.objects.all()
    return render(
        request,
        "core/sound_preferences.html",
        {"all_community_sounds": all_community_sounds},
    )


@authentication_required
def add_community_sound(request):
    if request.method == "POST":
        # get file from <input name="file"/>
        file = request.FILES["file"]
        # create new sound object
        Sound.objects.create(
            file=file,
        )

        messages.success(request, "sound added!")

        # redirect to avoid back-reload-resubmit issues
        return redirect("add_community_sound")

    return render(request, "core/add_community_sound.html")


@authentication_required
def delete_community_sound(request):
    if request.method == "POST":
        sound_id = request.POST.get("sound")

        sound_obj = Sound.objects.get(id=sound_id)

        # find all users that have a 'sound_preference' of 'single_sound' and this
        # sound set as 'single_sound_preference' and set their single_sound_preference to
        # none and their preference to 'random_community_sound'
        users_with_single_sound_preference = User.objects.filter(
            sound_preference="single_sound",
            single_sound_preference=sound_obj,
        )
        for user in users_with_single_sound_preference:
            user.sound_preference = "random_community_sound"
            user.single_sound_preference = None
            user.save()

        # delete file
        sound_obj.file.delete()
        sound_obj.delete()

        messages.success(request, "sound deleted!")

        # redirect to avoid back-reload-resubmit issues
        return redirect("delete_community_sound")

    all_community_sounds = Sound.objects.all()
    return render(
        request,
        "core/delete_community_sound.html",
        {"all_community_sounds": all_community_sounds},
    )
