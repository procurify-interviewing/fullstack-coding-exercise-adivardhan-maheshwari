.PHONY: setup reset reset-backend reset-frontend run run-backend run-frontend test-backend test-frontend

# Entry-point scripts in .venv/bin bake in an absolute shebang when the venv is
# created, so commands are invoked as modules through the interpreter instead.
PYTHON := .venv/bin/python

# manage.py runs with src/ as the working directory so that test discovery and
# app imports resolve; settings put db.sqlite3 in backend/ regardless.
MANAGE := cd backend/src && ../$(PYTHON) manage.py

# pytest.ini lives in backend/ and puts src/ on the path.
PYTEST := cd backend && $(PYTHON) -m pytest

# yarn.lock is the frontend lockfile, so scripts run through yarn.
YARN := yarn --cwd frontend

# Installs both halves, migrates and seeds the database.
setup:
	./setup.sh

# Deletes everything setup.sh creates so that `make setup` starts from a clean
# slate. Only generated artifacts are removed; tracked files are untouched.
reset: reset-backend reset-frontend
	@echo "Reset complete. Run 'make setup' to rebuild."

reset-backend:
	rm -rf backend/.venv backend/db.sqlite3 backend/.pytest_cache
	find backend -name __pycache__ -type d -prune -exec rm -rf {} +

reset-frontend:
	rm -rf frontend/node_modules frontend/dist

# Runs the API and the dev server together.
run:
	$(MAKE) -j2 run-backend run-frontend

run-backend:
	export DJANGO_RUNSERVER_HIDE_WARNING=true && $(MANAGE) runserver 8000

run-frontend:
	$(YARN) dev

test-backend:
	$(PYTEST)

test-frontend:
	$(YARN) typecheck
	$(YARN) test
