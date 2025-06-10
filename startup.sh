#!/bin/sh

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn HivePulse.wsgi:application \
    --config gunicorn_config.py
