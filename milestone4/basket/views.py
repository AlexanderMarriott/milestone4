from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket  # Ensure this import is correct
from shop.models import Product


def basket_summary(request):

    basket = Basket(request)

    return render(request, "basket/basket_summary.html", {"basket": basket})


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

        basket_quantity = basket.__len__()

        # Return a JSON response
        response = JsonResponse(
            {
                "qty": basket_quantity,
            }
        )
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)


def basket_delete(request):

    basket = Basket(request)

    if request.POST.get("action") == "post":

        product_id = int(request.POST.get('product_id'))

        basket.delete(product=product_id)

        basket_quantity = basket.__len__()

        basket_total = basket.get_total_price()

        response = JsonResponse({
            'qty': basket_quantity,
            'total': basket_total
        })

        return response




def basket_update(request):
    basket = Basket(request)

    if request.POST.get("action") == "post":

        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        basket.update(product=product_id, quantity=product_quantity)

        basket_quantity = basket.__len__()

        basket_total = basket.get_total_price()

        response = JsonResponse({
            'qty':basket_quantity,
            'total': basket_total
        })

        return response
