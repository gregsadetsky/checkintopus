import requests


class UnauthorizedError(Exception):
    pass


def _query(token, api_url, api_verb="GET", post_json={}):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://www.recurse.com/api/v1/{api_url}"

    if api_verb == "GET":
        r = requests.get(url, headers=headers)
    elif api_verb == "POST":
        r = requests.post(url, headers=headers, json=post_json)
    else:
        raise ValueError(f"Unknown API verb: {api_verb}")

    if not r.ok and r.json().get("message") == "unauthorized":
        raise UnauthorizedError()

    assert r.ok, f"Request failed: {r.text}"
    return r.json()


def get_profile(token):
    return _query(token, "profiles/me")
