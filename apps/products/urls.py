# ecom/apps/products/urls.py
from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("<int:id>/", views.product_detail, name="product_detail"),
]
