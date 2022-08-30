#!/bin/bash
source venv/Scripts/activate
cd backend/
alias python='winpty python.exe'
winpty python manage.py runserver localhost:8000
