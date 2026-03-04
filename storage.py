import sqlite3
import json
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "results.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            results TEXT,
            total INTEGER,
            passed INTEGER,
            failed INTEGER,
            avg_latency REAL,
            p95_latency REAL,
            error_rate REAL
        )
    """)
    # Migration : ajout des colonnes manquantes si ancienne version de la table
    existing = {row[1] for row in conn.execute("PRAGMA table_info(runs)")}
    for col, typedef in [("p95_latency", "REAL"), ("error_rate", "REAL")]:
        if col not in existing:
            conn.execute(f"ALTER TABLE runs ADD COLUMN {col} {typedef} DEFAULT 0")
    conn.commit()
    conn.close()


def _p95(latencies):
    if not latencies:
        return 0
    sorted_l = sorted(latencies)
    idx = int(len(sorted_l) * 0.95)
    return round(sorted_l[min(idx, len(sorted_l) - 1)], 2)


def save_run(results):
    init_db()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    latencies = [r["latency_ms"] for r in results]
    avg_latency = round(sum(latencies) / total, 2) if total > 0 else 0
    p95_latency = _p95(latencies)
    error_rate = round((failed / total) * 100, 1) if total > 0 else 0

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO runs
           (timestamp, results, total, passed, failed, avg_latency, p95_latency, error_rate)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (timestamp, json.dumps(results), total, passed, failed, avg_latency, p95_latency, error_rate)
    )
    conn.commit()
    conn.close()


def get_history(limit=10):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    history = []
    for row in rows:
        h = dict(row)
        h["results"] = json.loads(h["results"])
        h.setdefault("p95_latency", 0)
        h.setdefault("error_rate", 0)
        history.append(h)
    return history
