import time
from tester.client import get_age, get_batch, get_no_params

TESTS = []


def test(name):
    def decorator(fn):
        TESTS.append((name, fn))
        return fn
    return decorator


@test("Status 200 - prénom valide")
def test_status_ok():
    r = get_age("alice")
    assert r.status_code == 200, f"Attendu 200, reçu {r.status_code}"


@test("Structure JSON - clé 'name' présente")
def test_has_name():
    r = get_age("alice")
    assert "name" in r.json(), "Clé 'name' manquante"


@test("Structure JSON - clé 'age' présente")
def test_has_age():
    r = get_age("alice")
    assert "age" in r.json(), "Clé 'age' manquante"


@test("Type - 'age' est un entier")
def test_age_is_int():
    r = get_age("alice")
    age = r.json().get("age")
    assert isinstance(age, int), f"'age' devrait être int, reçu {type(age)}"


@test("Cohérence - 'name' correspond à la requête")
def test_name_matches():
    r = get_age("alice")
    assert r.json().get("name") == "alice", f"Nom retourné: {r.json().get('name')}"


@test("Temps de réponse < 3 secondes")
def test_response_time():
    start = time.time()
    get_age("alice")
    elapsed = time.time() - start
    assert elapsed < 3.0, f"Trop lent: {elapsed:.2f}s"


@test("Content-Type est application/json")
def test_content_type():
    r = get_age("alice")
    ct = r.headers.get("Content-Type", "")
    assert "application/json" in ct, f"Content-Type: {ct}"


@test("Requête batch - plusieurs prénoms")
def test_batch():
    r = get_batch(["alice", "bob", "charlie"])
    assert r.status_code == 200, f"Attendu 200, reçu {r.status_code}"
    data = r.json()
    assert isinstance(data, list), "La réponse batch devrait être une liste"
    assert len(data) == 3, f"Attendu 3 résultats, reçu {len(data)}"


@test("Filtre par pays - country_id=US")
def test_country_filter():
    r = get_age("john", country_id="US")
    assert r.status_code == 200, f"Attendu 200, reçu {r.status_code}"
    data = r.json()
    assert "age" in data, "Clé 'age' manquante avec filtre pays"


@test("Prénom inconnu - réponse valide (age nul)")
def test_unknown_name():
    r = get_age("xwqzplm123")
    assert r.status_code == 200, f"Attendu 200, reçu {r.status_code}"
    data = r.json()
    assert "age" in data, "Clé 'age' manquante pour prénom inconnu"
    assert data["age"] is None or isinstance(data["age"], int)
