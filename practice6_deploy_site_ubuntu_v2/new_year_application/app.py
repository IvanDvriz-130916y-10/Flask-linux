import os
from datetime import date
from pathlib import Path

from flask import Flask, abort, render_template, send_file
from werkzeug.utils import safe_join


def days_till_next_year(now=None):
    if now is None:
        now = date.today()
    target = date(now.year + 1, 1, 1)
    return (target - now).days


def make_app():
    app = Flask(__name__, static_folder=None)

    static_folder = Path(__file__).resolve().parent / "static"
    app.config["STATIC_DIR"] = str(static_folder)

    @app.get("/")
    def home():
        return render_template("index.html", days_left=days_till_next_year())

    @app.get("/static/<path:filename>")
    def serve_static(filename):
        base = app.config["STATIC_DIR"]
        safe_path = safe_join(base, filename)
        if safe_path is None or not os.path.isfile(safe_path):
            abort(404)
        return send_file(safe_path)

    return app


if __name__ == "__main__":
    make_app().run(host="0.0.0.0", port=8000, debug=False)