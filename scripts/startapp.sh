#!/bin/sh

set -e

while ! nc -z $DB_HOST_1 $DB_PORT_1; do
  echo "🟡 Waiting for Postgres Database Startup ($DB_HOST_1 $DB_PORT_1) ..."
  sleep 2
done



python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# python manage.py runserver 0.0.0.0:8000
gunicorn config.wsgi:application --bind 0.0.0.0:7002