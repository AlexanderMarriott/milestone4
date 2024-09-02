from django.shortcuts import render

# Create your views here.
from .models import Category, Product

from django.shortcuts import get_object_or_404


def store(request):

    all_products = Product.objects.all()

    context = {"all_products": all_products}

    return render(request, "shop/shop.html", context)


def categories(requests):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {"product": product}
    return render(request, "shop/product_detail.html", context)
