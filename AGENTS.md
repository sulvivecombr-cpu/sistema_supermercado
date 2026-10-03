# Base44 Dev Environment

Django 5.2 (MVT, server-rendered templates) + SQLite (`db.sqlite3`, committed, already migrated with demo data).

## Running

- `docker compose -f docker-compose.base44.yml up -d` — serves the app on port 3000.
- The compose service runs from the bind-mounted source with `manage.py runserver` (auto-reload on file edits). Dependencies are installed from `requirements.txt` (only Django) at container start.
- Migrations run on every boot (`migrate` is a no-op once applied). No seed step exists.

## Notes

- `ALLOWED_HOSTS = ['*']` in `sistema_supermercado/settings.py` — required because the preview proxy rewrites the Host header. The sandbox host rotates, so never pin an exact host.
- Routes: `/` (dashboard), `/entrega/` (stock intake, also updates existing product cost/sale price), `/caixa/` (POS/cart, session-backed, loyalty redemption 1pt=R$1 min 10), `/produtos|clientes|funcionarios/` (CRUD, admin login), `/vendas/` + `/vendas/<id>/` (sales history/detail), `/relatorios/`, `/admin/`.
- Admin-only pages are gated by `gestao.decorators.admin_required` (Django auth, is_staff). Cashier (`/caixa/`) and delivery are intentionally login-free.
- Dev admin user: `admin` (created via shell; password must be changed before real use).
- Timezone `America/Sao_Paulo`, locale pt-br. Product deletion is blocked when the product has sales/deliveries (history integrity).
- No external services or credentials are needed.
- Verify: `curl -f http://localhost:3000/` returns the dashboard HTML.
