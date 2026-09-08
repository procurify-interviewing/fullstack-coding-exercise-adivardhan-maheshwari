# Backend Project

A Django application backed by SQLite, Django REST Framework is installed and configured, but using it is optional.

See exercise brief in `[EXERCISE.md](EXERCISE.md)`. 

## Setup the project

From project root, `make setup` , which creates the virtualenv, installs dependencies, runs migrations, and seeds sample data.

## Running the project

Application code lives under `src/`. Run `manage.py` from there:

```bash
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
cd src
python manage.py runserver 8000
```

The `make` targets in the repo root (`make run-backend`, `make test-backend`) do this for you and do not need the virtualenv activated. 

## Database

`backend/db.sqlite3` database file, created by `python manage.py migrate`.

```bash
rm db.sqlite3
cd src && python manage.py migrate && python manage.py seed_data
```

## Tests

Run pytests from this directory, or with `make test-backend` from the repo root:

```bash
pytest src/tests/
```

