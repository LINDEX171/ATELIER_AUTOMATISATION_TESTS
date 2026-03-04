import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from tester.runner import run_all_tests
from storage import save_run

if __name__ == "__main__":
    results = run_all_tests()
    save_run(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"Run terminé : {passed}/{len(results)} tests passés")
