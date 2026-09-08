#!/usr/bin/env bash
# One-shot setup for macOS / Linux. Run from the repo root:
#   ./setup.sh
# Sets up the backend (venv, dependencies, migrations, seed data, tests)
# and the frontend (yarn dependencies, type check, tests).
set -euo pipefail

cd "$(dirname "$0")"
REPO_ROOT="$PWD"

find_python() {
  for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
        echo "$candidate"
        return 0
      fi
    fi
  done
  return 1
}

PY="$(find_python)" || {
  echo "Python 3.10 or newer is required and was not found on PATH." >&2
  echo "Install it from https://www.python.org/downloads/ and re-run ./setup.sh" >&2
  exit 1
}
echo "Using $($PY --version) at $(command -v "$PY")"

if ! command -v node >/dev/null 2>&1; then
  echo "Node 20 or newer is required and node was not found on PATH." >&2
  echo "Install it from https://nodejs.org/ and re-run ./setup.sh" >&2
  exit 1
fi
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$NODE_MAJOR" -lt 20 ]; then
  echo "Node 20 or newer is required; found $(node --version)." >&2
  echo "Install it from https://nodejs.org/ and re-run ./setup.sh" >&2
  exit 1
fi
echo "Using node $(node --version) at $(command -v node)"

# frontend/yarn.lock is the frontend lockfile, so the install runs through yarn.
if ! command -v yarn >/dev/null 2>&1; then
  echo "yarn is required and was not found on PATH." >&2
  echo "Install it with 'corepack enable' or 'npm install -g yarn', then re-run ./setup.sh" >&2
  exit 1
fi
echo "Using yarn $(yarn --version) at $(command -v yarn)"

echo
echo "Backend..."
cd "$REPO_ROOT/backend"
if [ ! -d .venv ]; then
  "$PY" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Installing dependencies.."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

cd src
python manage.py migrate --verbosity 0
python manage.py seed_data
echo "Data seeded: users, purchase requests, approvals"

cd ..
# The API test is an unimplemented stub, so a failing test here is expected.
# Anything other than "tests ran and some failed" is a real setup problem.
set +e
python -m pytest
PYTEST_STATUS=$?
set -e
if [ "$PYTEST_STATUS" -gt 1 ]; then
  echo "pytest could not run. The backend is not set up correctly." >&2
  exit "$PYTEST_STATUS"
fi

echo
echo "Frontend..."
cd "$REPO_ROOT"
# yarn v1 reports an unmet @babel/core peer dependency for every plugin the
# unused @babel/preset-* devDependencies pull in. Neither those nor the
# workspaces notice are actionable here, so they are filtered out.
yarn --cwd frontend install --frozen-lockfile 2>&1 \
  | sed -e '/has unmet peer dependency/d' -e '/Workspaces can only be enabled/d'

# The type check and the test suite are the two checks the exercise ships with;
# running them here surfaces a broken toolchain at setup rather than later.
yarn --cwd frontend typecheck
yarn --cwd frontend test

cat <<MSG

Setup complete.

Ready to start exercise in backend/EXERCISE.md and frontend/EXERCISE.md.

To run both backend/frontend project:

  make run

  Frontend  http://localhost:5173
  API       http://localhost:8000/api/purchase-requests/

MSG
