import datetime
from flask import Flask, render_template, jsonify, redirect, url_for
from tester.runner import run_all_tests
from storage import save_run, get_history

app = Flask(__name__)


@app.route("/")
def dashboard():
    history = get_history(limit=10)
    return render_template("dashboard.html", history=history)


@app.route("/run", methods=["POST"])
def run_tests():
    results = run_all_tests()
    save_run(results)
    return redirect(url_for("dashboard"))


@app.route("/api/results")
def api_results():
    history = get_history(limit=50)
    return jsonify(history)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "api_monitored": "https://api.agify.io"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
