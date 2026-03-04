import time
from tester.tests import TESTS


def run_all_tests():
    results = []
    for name, fn in TESTS:
        start = time.time()
        try:
            fn()
            passed = True
            message = "OK"
        except AssertionError as e:
            passed = False
            message = str(e)
        except Exception as e:
            passed = False
            message = f"{type(e).__name__}: {str(e)}"
        latency_ms = round((time.time() - start) * 1000, 2)
        results.append({
            "name": name,
            "passed": passed,
            "message": message,
            "latency_ms": latency_ms
        })
    return results
