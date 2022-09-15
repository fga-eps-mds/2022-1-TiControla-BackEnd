#!/bin/bash

sleep 30
python manage.py flush --no-input
python manage.py migrate
./manage.py createsuperuser --no-input --email=${DJANGO_SUPERUSER_EMAIL}
gunicorn core.wsgi:application --bind :8080 --workers 3
