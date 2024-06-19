# ecom/apps/products/urls.py
from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
    path("<int:product_id>/rate/", views.rate_product, name="rate_product"),  # New URL pattern for rating

]
