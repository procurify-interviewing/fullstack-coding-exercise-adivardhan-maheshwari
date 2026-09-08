# Interview Exercise - Purchase Requests

A small Django + React project that serves an API endpoint and the React app for the coding exercise.

## Goal

Implement the Purchase Requests API in `backend/`, then build a React component in
`frontend/` that consumes it.

- [backend/EXERCISE.md](backend/EXERCISE.md)
- [frontend/EXERCISE.md](frontend/EXERCISE.md)

## Timeline

| Stage | Time | What |
| ----- | ---- | ---- |
| Backend | 50 min | Purchase Requests API - 2 parts |
| Frontend | 35 min | React Component - 2 parts |
| Demo | 10 min | Walk through what you built |


## Setup

From the repo root:

```bash
make setup
```

On Windows PowerShell, run `.\setup.ps1` instead - `make setup` shells out to `setup.sh`.

To start over, `make reset` deletes everything setup creates - the virtualenv, the SQLite
database, caches, and `node_modules` - so `make setup` runs from a clean slate.

(Requires Python 3.10 or newer, Node 20 or newer, and yarn)

## Run

```bash
make run            # API on :8000 and dev server on :5173
make run-backend    # API only
make run-frontend   # dev server only
make test-backend
make test-frontend
```

| Service  | URL |
| -------- | --- |
| Frontend | [http://localhost:5173](http://localhost:5173) |
| API      | [http://localhost:8000/api/purchase-requests/](http://localhost:8000/api/purchase-requests/) |

