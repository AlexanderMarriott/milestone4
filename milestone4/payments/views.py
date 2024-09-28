from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from basket.basket import Basket
from django.http import JsonResponse

def checkout(request):

    #prefill the form with the user's saved info

    if request.user.is_authenticated:

        try:
            #authenticated user WITH shipping info

            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context = {
                "shipping": shipping_address,
            }

            return render(request, "payments/checkout.html", context=context)

        except:

            #authenticated user WITHOUT shipping info
            return render(request, "payments/checkout.html")

            
    else:

        return render(request, "payments/checkout.html")
    

def complete_order(request):
    if request.POST.get('action') == 'post':
    
            #get the form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            country = request.POST.get('country')
            postal_code = request.POST.get('postal_code')

            #style the shipping address
            shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + country + "\n" + postal_code)

            #basket info
            basket = Basket(request)

            total_cost = basket.get_total_price()

            if request.user.is_authenticated:
                order = Order.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=total_cost,
                    user=request.user
                )

                order_id = order.pk

                for item in basket:
                    OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],  
                    quantity=item['quantity'],
                    price=item['price'],
                    user=request.user
                )
            else:
  
                order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost
                 )

                order_id = order.pk

                for item in basket:
                    OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],  
                    quantity=item['quantity'],
                    price=item['price']
                    )

            order_success = True

            response = JsonResponse({'success': order_success})

            return response
    




def payment_success(request):

    #clear the basket

    for key in list(request.session.keys()):
        if key == 'sKey':
            del request.session[key]
    return render(request, "payments/payment-success.html")

def payment_failed(request):
    return render(request, "payments/payment-failed.html")

