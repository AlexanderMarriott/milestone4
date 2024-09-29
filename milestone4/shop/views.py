from django.shortcuts import render

# Create your views here.
from .models import Category, Product

from django.shortcuts import get_object_or_404


def store(request):

    all_products = Product.objects.all()

    for product in all_products:
        print(product.image.url)

    context = {"all_products": all_products}

    return render(request, "shop/shop.html", context)


def categories(requests):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


def list_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {"category": category, "products": products}
    return render(request, "shop/list_category.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {"product": product}
    return render(request, "shop/product_detail.html", context)
