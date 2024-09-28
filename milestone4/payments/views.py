from django.shortcuts import render
from .models import ShippingAddress

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


def payment_success(request):
    return render(request, "payments/payment-success.html")

def payment_failed(request):
    return render(request, "payments/payment-failed.html")

