# otel-sample-python-app

Two Python microservices (service-a UI + service-b API) backed by Postgres.

## Quick start

```bash
docker compose up --build
```

Open the UI:

- http://localhost:8000

To verify service-b directly:

- http://localhost:8001/events

## What this demo does

- `service-a` renders a UI and writes a row to Postgres on form submit.
- `service-a` calls `service-b` to fetch recent rows.

## Components

- `services/service_a`: Flask UI + DB write + downstream request
- `services/service_b`: Flask API + DB read
- `docker-compose.yml`: Postgres + services

## Notes

- The database table is created automatically on the first request.
