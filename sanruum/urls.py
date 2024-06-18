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
