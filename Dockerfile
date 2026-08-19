FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements /app/requirements
RUN pip install --no-cache-dir -r /app/requirements/base.txt

COPY backend/ /app/

# Collect static using local settings (no production secrets/DB required at build).
RUN SECRET_KEY=build-time-collectstatic python manage.py collectstatic --noinput

EXPOSE 8000

# Production platforms must set DJANGO_SETTINGS_MODULE=core.settings.production.
# docker-compose overrides this for the local Celery worker.
ENV DJANGO_SETTINGS_MODULE=core.settings.production

CMD ["gunicorn", "core.wsgi:application", "--config", "gunicorn.conf.py"]
