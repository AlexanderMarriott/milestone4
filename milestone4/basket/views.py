from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket  
from shop.models import Product
from django.contrib import messages


def basket_summary(request):

    basket = Basket(request)

    return render(request, "basket/basket_summary.html", {"basket": basket})



def basket_add(request):
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity"))

        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=quantity)

        basket_quantity = basket.__len__()

        # Add success message
        messages.success(request, 'Item successfully added to the cart!')

        response = JsonResponse({
            'qty': basket_quantity,


        })
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)



def basket_delete(request):
    basket = Basket(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get('product_id'))

        basket.delete(product_id=product_id)

        basket_quantity = basket.__len__()
        basket_total = basket.get_total_price()

        messages.success(request, 'Item successfully removed from cart!')

        response = JsonResponse({
            'qty': basket_quantity,
            'total': basket_total
        })

        return response

    return JsonResponse({"error": "Invalid request"}, status=400)





def basket_update(request):
    basket = Basket(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        basket.update(product_id=product_id, quantity=product_quantity)

        basket_quantity = basket.__len__()
        basket_total = basket.get_total_price()

        messages.success(request, 'Quantity Updated!')

        response = JsonResponse({
            'qty': basket_quantity,
            'total': basket_total
        })

        return response

    return JsonResponse({"error": "Invalid request"}, status=400)
