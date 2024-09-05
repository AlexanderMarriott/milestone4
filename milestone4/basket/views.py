from django.shortcuts import render

from .basket import basket

from shop.models import Product

from django.shortcuts import get_object_or_404


def basket_summary(request):
    return render(request, "basket/basket_summary.html")


def basket_add(request):
    basket = basket(request)

    if request.post.get("action") == "post":
        product_id = int(request.post.get("product_id"))
        quantity = int(request.post.get("quantity"))

        product = get_object_or_404(Product, id=product_id)

        basket.add(product=product, quantity=quantity)


def basket_delete(request):
    pass


def basket_update(request):
    pass
