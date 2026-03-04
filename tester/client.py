import requests

BASE_URL = "https://api.agify.io"
TIMEOUT = 5


def get_age(name, country_id=None):
    params = {"name": name}
    if country_id:
        params["country_id"] = country_id
    return requests.get(BASE_URL, params=params, timeout=TIMEOUT)


def get_batch(names):
    params = [("name[]", n) for n in names]
    return requests.get(BASE_URL, params=params, timeout=TIMEOUT)


def get_no_params():
    return requests.get(BASE_URL, timeout=TIMEOUT)
