#!/bin/sh
set -e

attempt=1
max_attempts=30
until python manage.py migrate --noinput; do
    if [ "$attempt" -ge "$max_attempts" ]; then
        echo "Database migration failed after $max_attempts attempts."
        exit 1
    fi
    echo "Database not ready yet (attempt $attempt/$max_attempts), retrying in 2s..."
    attempt=$((attempt + 1))
    sleep 2
done

exec python manage.py runserver 0.0.0.0:8000
