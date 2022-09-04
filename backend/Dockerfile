FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip && pip3 install -r /app/backend/requirements.txt --no-cache-dir

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000