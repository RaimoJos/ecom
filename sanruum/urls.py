# ecom/sanruum/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", include("apps.products.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("orders/", include("apps.orders.urls")),
    path("cart/", include("apps.cart.urls")),
    path("favorites/", include("apps.favorites.urls")),
    path("delivery/", include("apps.delivery.urls")),
    path("support/", include("apps.support.urls")),
]
