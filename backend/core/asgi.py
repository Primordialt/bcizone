"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Default is local. Production must set DJANGO_SETTINGS_MODULE=core.settings.production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

application = get_asgi_application()
