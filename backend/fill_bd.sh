#!/bin/bash
python manage.py makemigrations api
python manage.py makemigrations users
python manage.py makemigrations recipes
python manage.py migrate
python manage.py collectstatic
python ./manage.py loaddata db.json