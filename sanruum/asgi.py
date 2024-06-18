# ecom/sanruum/asgi.py
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sanruum.settings")

application = get_asgi_application()
