#!/bin/sh
set -e

# Run DB migrations then start the server
if [ -n "$DATABASE_URL" ]; then
  echo "Running alembic migrations..."
  # ensure the project root is on PYTHONPATH so `import app` works
  export PYTHONPATH="/app:${PYTHONPATH}"
  alembic upgrade head || true
fi

echo "Starting uvicorn..."
exec gunicorn -k uvicorn.workers.UvicornWorker app.main:app -w ${WORKERS:-4} -b 0.0.0.0:8000 --log-level info
