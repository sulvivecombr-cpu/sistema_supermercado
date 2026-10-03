# Base44 Dev Environment

Django 5.2 (MVT, server-rendered templates) + SQLite (`db.sqlite3`, committed, already migrated with demo data).

## Running

- `docker compose -f docker-compose.base44.yml up -d` — serves the app on port 3000.
- The compose service runs from the bind-mounted source with `manage.py runserver` (auto-reload on file edits). Dependencies are installed from `requirements.txt` (only Django) at container start.
- Migrations run on every boot (`migrate` is a no-op once applied). No seed step exists.

## Notes

- `ALLOWED_HOSTS = ['*']` in `sistema_supermercado/settings.py` — required because the preview proxy rewrites the Host header. The sandbox host rotates, so never pin an exact host.
- Routes: `/` (dashboard), `/entrega/` (stock intake), `/caixa/` (POS/cart, session-backed), `/admin/`.
- No external services or credentials are needed.
- Verify: `curl -f http://localhost:3000/` returns the dashboard HTML.
