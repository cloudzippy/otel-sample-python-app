# Repository Guidelines

## Project Structure & Module Organization

- `services/service_a`: Flask UI service, HTML templates in `services/service_a/templates`.
- `services/service_b`: Flask API service.
- `docker-compose.yml`: Orchestration for services and Postgres.
- `README.md`: Quick-start and usage notes.

There is no dedicated `tests/` directory at this time.

## Build, Test, and Development Commands

- `docker compose up --build`
  Builds images and starts Postgres plus both services.
- `docker compose up`
  Starts using existing images.
- `docker compose down -v`
  Stops services and removes volumes (reset data).

Local (non-Docker) runs are possible but not standardized; prefer Docker for consistency.

## Coding Style & Naming Conventions

- Python: 4-space indentation, PEP 8 style.
- Use snake_case for functions/variables (e.g., `create_app`, `db_url`).
- HTTP routes are lowercase with hyphens only if needed.
- HTML templates belong under `services/service_a/templates`.

There is no formatter or linter configured yet; keep changes minimal and consistent with existing style.

## Testing Guidelines

No automated tests are configured. If you add tests, place them under `tests/` and document how to run them in `README.md`.

## Commit & Pull Request Guidelines

- Commit messages are concise and imperative (e.g., `Remove OpenTelemetry components`).
- Keep commits focused on a single logical change.

For pull requests:
- Provide a clear description of the change and its intent.
- Include how to run or validate the change (commands or expected behavior).
- Add screenshots for UI changes (service-a).

## Configuration & Data

- Postgres connection is configured via `DATABASE_URL` in `docker-compose.yml`.
- Data persists in Docker volumes unless removed with `docker compose down -v`.
