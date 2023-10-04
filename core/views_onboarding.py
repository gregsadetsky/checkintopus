from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import RFIDTagScanLog
from .views_utils import oauth_required


@oauth_required
def onboarding(request, **_):
    # get all logs for which an 'unknown_card_random_name' has been generated
    # in the last 5 minutes and list them in date desc order
    recent_unknown_card_scans = RFIDTagScanLog.objects.filter(
        unknown_card_random_name__isnull=False,
        scan_time__gte=datetime.now() - timedelta(minutes=5),
    ).order_by("-scan_time")

    return render(
        request,
        "core/onboarding.html",
        {"recent_unknown_card_scans": recent_unknown_card_scans},
    )


@require_http_methods(["POST"])
def onboarding_confirm_card(request):
    # get <button name='rfid_card_scan_id' value='(int)'> value
    rfid_card_scan_id = request.POST.get("rfid_card_scan_id")
    found_rfid_card_scan_obj = get_object_or_404(RFIDTagScanLog, pk=rfid_card_scan_id)

    # we are ready to associate the user with the scanned rfid card's fc + card id
    request.user.rfid_tag_fc = found_rfid_card_scan_obj.rfid_tag_fc
    request.user.rfid_tag_card = found_rfid_card_scan_obj.rfid_tag_card
    request.user.save()

    # done!! redirect to homepage
    return redirect("index")
