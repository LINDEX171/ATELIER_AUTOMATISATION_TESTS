import time
import requests

BASE_URL = "https://api.agify.io"
TIMEOUT = 5
MAX_RETRIES = 1


def _get(params):
    """Appel HTTP avec timeout, retry et gestion 429/5xx."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            r = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
            if r.status_code == 429:
                # Rate limit : on attend 2s et on réessaie
                time.sleep(2)
                continue
            if r.status_code >= 500 and attempt < MAX_RETRIES:
                # Erreur serveur : on réessaie une fois
                time.sleep(1)
                continue
            return r
        except requests.Timeout:
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            raise
    return r


def get_age(name, country_id=None):
    params = {"name": name}
    if country_id:
        params["country_id"] = country_id
    return _get(params)


def get_batch(names):
    params = [("name[]", n) for n in names]
    return _get(params)


def get_no_params():
    return _get({})
