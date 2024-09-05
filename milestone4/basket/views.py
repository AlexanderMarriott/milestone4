from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket  # Ensure this import is correct
from shop.models import Product


def basket_summary(request):
    return render(request, "basket/basket_summary.html")


def basket_add(request):
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity"))

        # Initialize the basket
        basket = Basket(request)

        # Get the product
        product = get_object_or_404(Product, id=product_id)

        # Add the product to the basket
        basket.add(product=product, quantity=quantity)

        # Return a JSON response
        response = JsonResponse(
            {
                "The product is called": product.title,
                "and the product quantity is": quantity,
            }
        )
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)


def basket_delete(request):
    pass


def basket_update(request):
    pass
