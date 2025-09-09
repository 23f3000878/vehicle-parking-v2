# Vehicle Parking App (vehicle-parking-v2)

A multi-user vehicle parking management application built with **Flask** (backend), **Vue 3** + Vite (frontend), **Celery** + **Redis** (background jobs & scheduling), **Flask-Mail** (email), and **flask-jwt-extended** (authentication). The app supports an Admin (single superuser) and Users who can register, book and release parking spots. SQLite is used for local persistence.

---

## Features

* Admin role with full control (create/edit/delete parking lots, view users, view spot status)
* User role with register/login, reserve first-available spot, release spot
* Automatic creation of parking spots when an admin creates a lot (based on `number_of_spots`)
* Booking history and CSV export (export is performed as a background task)
* Periodic background jobs (Celery Beat): daily reminders and monthly activity reports (sent by email)
* Caching using Redis for performance-sensitive endpoints
* JWT-based authentication with role checks

---

## Repo structure (top-level)

```
.
├── backend
│   ├── app.py
│   ├── celery_app.py
│   ├── celery_worker.py
│   ├── config.py
│   ├── controllers/ (auth, user, admin, ...)
│   ├── model.py
│   ├── tasks.py
│   ├── extensions.py
│   └── requirements.txt
└── frontend
    ├── index.html
    ├── src/ (App.vue, components, views, router, services)
    ├── package.json
    └── vite.config.js
```

---

## Quick local development (Linux / macOS)

**Prerequisites**: Python 3.10+, Node (pnpm recommended), Redis.

1. Start Redis: `redis-server` (or run via Docker)

2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# create a .env file (example below)
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

3. Start Celery worker and beat (two terminals)

```bash
# terminal 1
source .venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info

# terminal 2
source .venv/bin/activate
celery -A celery_worker.celery beat --loglevel=info
```

4. Frontend

```bash
cd frontend
pnpm i
pnpm dev
```

The frontend (Vite) will typically run at `http://localhost:5173` and the backend at `http://localhost:5000`.

---

## Example `.env` (backend/.env)

```
FLASK_ENV=development
SECRET_KEY=replace_with_random
SQLALCHEMY_DATABASE_URI=sqlite:///app.sqlite3
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
JWT_SECRET_KEY=replace_with_jwt_secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

> If using Gmail, create an app password and use that as `MAIL_PASSWORD`.

---

## Celery schedule (example)

Add periodic schedules in `celery_app.py` or `celery_worker.py`:

```python
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'daily-reminder-every-18': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),
    },
    'monthly-report': {
        'task': 'tasks.generate_send_monthly_reports',
        'schedule': crontab(hour=1, minute=0, day_of_month='1'),
    }
}
```

---

## Export (CSV) flow

1. User requests export via frontend (POST `/api/exports`)
2. Backend enqueues `tasks.export_user_bookings(user_id)` in Celery and returns task id (202)
3. Celery task generates CSV in `backend/exports/` and updates task metadata (or emails the user a link)
4. Frontend may poll `/api/tasks/<task_id>` to get status or rely on email notification

---

## Important notes and caveats

* **SQLite + Celery**: SQLite is file-based and can cause `database is locked` errors with concurrent writers (Flask + Celery). For robust concurrent behavior, use PostgreSQL for production or when running workers and web server simultaneously.
* **CORS**: Enable CORS on the backend for your frontend origin (Vite: `http://localhost:5173`).
* **Security**: Use short-lived access tokens and refresh tokens. Use HTTPS for production, store secrets safely.
* **Email**: If emails don't send, check SMTP settings and ports and ensure no firewall blocks outbound SMTP.

---

## Docker (development) — notes

You can use a `docker-compose.yml` with services: `redis`, `backend`, `worker`, `beat`, `frontend`. Keep volumes mapped for live code reload while developing. A sample compose file is useful — ask if you want a ready-to-use one.

---

## Tests & improvements (recommended)

* Add unit tests for booking, releasing and export flows.
* Use Flask-Migrate for schema migrations.
* Add Flask-Caching (Redis) for frequently-read endpoints (lot lists, stats).
* Add input validation (Marshmallow) and rate-limiting on auth endpoints.

---

## How to create admin (helper)

Add a small script to programmatically create the single admin user after DB init (example: `scripts/create_admin.py`).

---

## License & Credits

This project is part of an academic project assignment.
