from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Rating


def home(request):
    print("Current language code:", request.LANGUAGE_CODE)
    return render(request, "home.html")


def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {'product': product})


@login_required
def rate_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        rating_value = request.POST.get("rating")
        if rating_value in ["1", "2", "3", "4", "5"]:
            try:
                rating, created = Rating.objects.get_or_create(product=product, user=request.user)
                rating.rating = int(rating_value)
                rating.save()
                messages.success(request, "Rating submitted successfully.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Invalid rating value.")
    return redirect("products:product_detail", product_id=product.id)
