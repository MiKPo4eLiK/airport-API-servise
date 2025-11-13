#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for database..."
python manage.py wait_for_db

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn airport_service.wsgi:application --bind 0.0.0.0:8000
