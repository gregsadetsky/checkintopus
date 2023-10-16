def is_rc_profile_staff(rc_profile):
    if rc_profile.get("stints"):
        active_stints = filter(
            lambda stint: stint["in_progress"] is True, rc_profile["stints"]
        )
        for stint in active_stints:
            if stint["type"] == "employment":
                return True
    return False


def get_latest_batch_name(rc_profile):
    if rc_profile.get("stints"):
        filtered_stints = filter(lambda _: _["type"] == "retreat", rc_profile["stints"])
        # sort by descending batch id
        sorted_stints = sorted(
            list(filtered_stints), reverse=True, key=lambda _: _.get("id", -1)
        )
        if len(sorted_stints) > 0:
            return sorted_stints[0]["batch"]["name"]
    return None
