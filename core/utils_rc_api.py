from datetime import datetime

import pytz
import requests


class UnauthorizedError(Exception):
    pass


def _query(token, api_url, api_verb="GET", post_json={}):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://www.recurse.com/api/v1/{api_url}"

    if api_verb == "GET":
        r = requests.get(url, headers=headers)
    elif api_verb == "PATCH":
        r = requests.patch(url, headers=headers, json=post_json)
    elif api_verb == "DELETE":
        r = requests.delete(url, headers=headers, json=post_json)
    else:
        raise ValueError(f"Unknown API verb: {api_verb}")

    if not r.ok and r.json().get("message") == "unauthorized":
        raise UnauthorizedError()

    assert r.ok, f"Request failed: {r.text}"

    # delete methods don't return anything
    if api_verb == "DELETE":
        return {}

    return r.json()


def _get_formatted_today_date_in_new_york():
    # get current day in new york
    day_in_new_york = datetime.now(tz=pytz.timezone("US/Eastern"))
    return day_in_new_york.strftime("%Y-%m-%d")


def create_hub_visit_for_today(token, user_id):
    day_in_new_york_formatted = _get_formatted_today_date_in_new_york()
    return _query(
        token, f"/hub_visits/{user_id}/{day_in_new_york_formatted}", api_verb="PATCH"
    )


def delete_hub_visit_for_today(token, user_id):
    day_in_new_york_formatted = _get_formatted_today_date_in_new_york()
    return _query(
        token, f"/hub_visits/{user_id}/{day_in_new_york_formatted}", api_verb="DELETE"
    )


def list_visits_for_user(token, user_id):
    # filter by given user_id
    return _query(token, f"/hub_visits?person_id={user_id}")


def get_profile(token):
    return _query(token, "profiles/me")
