# ecom/apps/products/

## migrations/

## __init__.py

```
# ecom/apps/products/__init__.py

```

## admin.py

```
# ecom/apps/products/admin.py
from django.contrib import admin

# Register your models here.

```

## apps.py

```
# ecom/apps/products/apps.py
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

```

## models.py

```
# ecom/apps/products/models.py
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

```

## urls.py

```
# ecom/apps/products/urls.py
from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("<int:id>/", views.product_detail, name="product_detail"),
]

```

## views.py

```
from django.shortcuts import render, get_object_or_404

from .models import Product


def home(request):
    return render(request, "home.html")


def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {'product': product})

```

# ecom/apps/support/

## ecom/apps/support/managment/commands/runsslserver.py

```
# ecom/apps/support/management/commands/runsslserver.py
import logging
import ssl

from django.core.management.base import BaseCommand
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler
from django.core.wsgi import get_wsgi_application

logging.basicConfig(level=logging.DEBUG)


class SSLWSGIServer(WSGIServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='ssl/cert.pem', keyfile='ssl/key.pem')
        self.socket = context.wrap_socket(self.socket, server_side=True)
        logging.debug("SSLWSGIServer initialized with SSL context")


class Command(BaseCommand):
    help = 'Run a development server with SSL.'

    def add_arguments(self, parser):
        parser.add_argument('addr', nargs='?', default='127.0.0.1', help='Optional IP address to bind to.')
        parser.add_argument('port', nargs='?', type=int, default=8000, help='Optional port number, defaults to 8000.')

    def handle(self, *args, **options):
        addr = options['addr']
        port = options['port']
        self.stdout.write(f"Starting development server at https://{addr}:{port}\n")
        self.stdout.write("Using SSL certificate from ssl/cert.pem and ssl/key.pem\n")

        handler = get_wsgi_application()
        logging.debug("WSGI application loaded")

        server_address = (addr, port)
        httpd = SSLWSGIServer(server_address, WSGIRequestHandler)
        httpd.set_app(handler)
        logging.debug("SSLWSGIServer ready to serve")

        httpd.serve_forever()

```

## migrations/

## __init__.py

```
# ecom/apps/support/__init__.py

```

## admin.py

```
# ecom/apps/support/admin.py
from django.contrib import admin

# Register your models here.

```

## apps.py

```
# ecom/apps/support/apps.py
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.support"

```

## models.py

```
# ecom/apps/support/models.py
from django.db import models

# Create your models here.

```

## urls.py

```
# ecom/apps/support/urls.py

app_name = "support"

urlpatterns = [

]

```

## views.py

```
# ecom/apps/support/views.py
from django.shortcuts import render


def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

```

# Project files(settings and other needed)

# ecom/sanruum/

## ecom/sanruum/__init__.py

```
# ecom/sanruum/__init__.py

```

## ecom/sanruum/asgi.py

```
# ecom/sanruum/asgi.py
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sanruum.settings")

application = get_asgi_application()
```

## ecom/sanruum/settings.py

```
# ecom/sanruum/settings.py
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the log file path
LOG_FILE_PATH = os.path.join(BASE_DIR / "docs", "logs", "django.log")

load_dotenv(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party apps
    "rest_framework",
    "rest_framework.authtoken",

    # Local apps
    "apps.products",
    # "apps.accounts",
    # "apps.orders",
    # "apps.cart",
    # "apps.favorites",
    # "apps.delivery",
    "apps.support",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sanruum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sanruum.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGES = [
    ("en", _("English")),
    ("et", _("Estonian")),
    ("ru", _("Russian"))
]
TIME_ZONE = "Europe/Tallinn"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Set the logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOG_FILE_PATH,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

if DEBUG:
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
else:
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

```

## ecom/sanruum/urls.py

```
# ecom/sanruum/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

handler404 = "apps.support.views.custom_404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", include("apps.products.urls")),
    # path("accounts/", include("apps.accounts.urls")),
    # path("orders/", include("apps.orders.urls")),
    # path("cart/", include("apps.cart.urls")),
    # path("favorites/", include("apps.favorites.urls")),
    # path("delivery/", include("apps.delivery.urls")),
    path("support/", include("apps.support.urls")),
    path('', TemplateView.as_view(template_name='home.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

## ecom/sanruum/wsgi.py

```
# ecom/sanruum/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sanruum.settings")

application = get_wsgi_application()

```

# ecom/ssl/

## ecom/ssl/cert.pem

## ecom/ssl/key.pem

# ecom/

## .gitignore

```
docs/logs/
docs/project_docs/
db.sqlite3
.env
```

## db.sqlite3

## manage.py

```
# ecom/manage.py
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanruum.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as RunserverCommand

        # Check if 'runsslserver' is in the command-line arguments
        if 'runsslserver' in sys.argv:
            try:
                from apps.support.management.commands.runsslserver import Command as SSLServerCommand
                # Replace the default RunserverCommand with SSLServerCommand
                RunserverCommand = SSLServerCommand
            except ModuleNotFoundError as e:
                print(f"Error: {e}")
                print("Ensure the runsslserver command exists and the directory structure is correct.")
                sys.exit(1)

        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()

```

## README.md

## requirements.txt

```
Django==5.0.6
python-dotenv==1.0.1
```
