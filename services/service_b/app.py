import os
import time
from datetime import datetime

from flask import Flask, request
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
        if not getattr(app, "_schema_ready", False):
            init_db()
            app._schema_ready = True

    @app.route("/events")
    def events():
        limit = int(request.args.get("limit", "5"))
        with engine.begin() as conn:
            rows = conn.execute(
                text(
                    "SELECT id, source, message, created_at FROM demo_events ORDER BY id DESC LIMIT :l"
                ),
                {"l": limit},
            ).mappings()
            items = [
                {
                    "id": r["id"],
                    "source": r["source"],
                    "message": r["message"],
                    "created_at": r["created_at"].isoformat(),
                }
                for r in rows
            ]

        return {
            "service": "service-b",
            "count": len(items),
            "items": items,
            "time": datetime.utcnow().isoformat() + "Z",
        }

    @app.route("/healthz")
    def healthz():
        return {"status": "ok", "service": "service-b", "time": time.time()}

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "8001"))
    app.run(host="0.0.0.0", port=port)
