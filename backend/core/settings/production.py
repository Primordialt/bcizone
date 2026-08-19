"""
Production settings.

Requires DJANGO_SETTINGS_MODULE=core.settings.production and the environment
variables documented in backend/.env.example. Do not use this module locally.
"""

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY or SECRET_KEY.startswith("django-insecure"):
    raise ImproperlyConfigured("Production SECRET_KEY must be a strong env value.")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    raise ImproperlyConfigured("ALLOWED_HOSTS must be set for production.")

# PostgreSQL via DATABASE_URL. SQLite is rejected.
DATABASES = {"default": env.db("DATABASE_URL")}
_engine = DATABASES["default"].get("ENGINE", "")
if "sqlite" in _engine:
    raise ImproperlyConfigured(
        "Production must not use SQLite. Set DATABASE_URL to a PostgreSQL URL."
    )

# No localhost fallbacks — set the real frontend origin(s) at deploy time.
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

REDIS_URL = env("REDIS_URL")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Reverse-proxy TLS termination (Render, nginx, load balancer, etc.).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# Platform health probes typically hit HTTP on PORT; do not 301 them to HTTPS.
SECURE_REDIRECT_EXEMPT = [r"^health/$"]
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"

# Keep /api/test-error/ off unless explicitly enabled for a Sentry check.
ENABLE_SENTRY_TEST_ENDPOINT = env.bool("ENABLE_SENTRY_TEST_ENDPOINT", default=False)
