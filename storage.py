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
            avg_latency REAL
        )
    """)
    conn.commit()
    conn.close()


def save_run(results):
    init_db()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    avg_latency = round(sum(r["latency_ms"] for r in results) / total, 2) if total > 0 else 0

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO runs (timestamp, results, total, passed, failed, avg_latency) VALUES (?, ?, ?, ?, ?, ?)",
        (timestamp, json.dumps(results), total, passed, failed, avg_latency)
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
        history.append(h)
    return history
