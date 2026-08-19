"""Gunicorn process settings for the Django API."""

import os

# Render sets PORT. GUNICORN_BIND still wins when explicitly set.
# Local default remains 0.0.0.0:8000.
_port = os.environ.get("PORT", "8000")
bind = os.environ.get("GUNICORN_BIND", f"0.0.0.0:{_port}")
workers = int(os.environ.get("GUNICORN_WORKERS", "3"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))
accesslog = "-"
errorlog = "-"
capture_output = True
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
