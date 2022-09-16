#!/bin/bash

sleep 30
python3 manage.py makemigrations
python3 manage.py makemigrations user
python3 manage.py makemigrations user_data
python3 manage.py makemigrations cartao
python3 manage.py makemigrations gastos

python manage.py flush --no-input
python manage.py migrate
./manage.py createsuperuser --no-input --email=${DJANGO_SUPERUSER_EMAIL}
gunicorn core.wsgi:application --bind :8080 --workers 3
