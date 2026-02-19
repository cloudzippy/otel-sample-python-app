import os
import time
from datetime import datetime

import requests
from flask import Flask, render_template, request
from sqlalchemy import create_engine, text


def create_app():
    app = Flask(__name__)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required")

    engine = create_engine(db_url, pool_pre_ping=True)

    def init_db():
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS demo_events (
                        id SERIAL PRIMARY KEY,
                        source VARCHAR(64) NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
            )

    @app.before_request
    def ensure_schema():
        # lightweight init check on first request
        if not getattr(app, "_schema_ready", False):
            init_db()
            app._schema_ready = True

    @app.route("/", methods=["GET", "POST"])
    def index():
        action_result = None
        if request.method == "POST":
            msg = request.form.get("message") or "hello from service-a"
            with engine.begin() as conn:
                conn.execute(
                    text("INSERT INTO demo_events (source, message) VALUES (:s, :m)"),
                    {"s": "service-a", "m": msg},
                )
            action_result = f"Inserted event at {datetime.utcnow().isoformat()}Z"

        # call service-b to enrich the trace with a downstream span
        service_b_url = os.getenv("SERVICE_B_URL", "http://service-b:8001")
        try:
            resp = requests.get(f"{service_b_url}/events", timeout=2)
            resp.raise_for_status()
            downstream = resp.json()
        except Exception as exc:  # noqa: BLE001
            downstream = {"error": str(exc)}

        return render_template(
            "index.html",
            action_result=action_result,
            downstream=downstream,
        )

    @app.route("/healthz")
    def healthz():
        return {"status": "ok", "service": "service-a", "time": time.time()}

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
