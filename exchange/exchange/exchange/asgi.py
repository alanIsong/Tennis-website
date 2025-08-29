"""
ASGI setup for The Tennis Exchange project.

This file exposes the ASGI callable as a module-level variable named ``application``.
For details, see:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange.settings")

application = get_asgi_application()